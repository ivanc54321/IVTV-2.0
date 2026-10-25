"""
Automated Verification Script for IVTV Accounts & Cloud Storage Endpoints
"""
import urllib.request
import urllib.parse
import json

BASE_URL = "http://127.0.0.1:5173"

def request_json(path, method="GET", payload=None, token=None):
    url = f"{BASE_URL}{path}"
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    with urllib.request.urlopen(req, timeout=5) as res:
        return res.status, json.loads(res.read().decode("utf-8"))

def run_tests():
    print("=== Testing IVTV Auth & Stored Favorites Endpoints ===")
    import user_db
    with user_db.get_connection() as conn:
        conn.execute("DELETE FROM users WHERE username = ?", ("sky_fan_01",))
        conn.commit()

    # 1. Register a test user with initial favorites
    print("\n1. Testing Register...")
    reg_payload = {
        "username": "sky_fan_01",
        "password": "mypassword123",
        "displayName": "Sky Premier VIP",
        "avatar": "cyber-crown",
        "initialFavorites": ["sky-atlantic-uk", "sky-cinema-premiere-uk"]
    }
    status, reg_res = request_json("/api/auth/register", "POST", reg_payload)
    assert status == 200, f"Expected 200, got {status}"
    assert reg_res["success"] is True
    assert reg_res["user"]["username"] == "sky_fan_01"
    token = reg_res["token"]
    print("[OK] Registration successful! User ID:", reg_res["user"]["id"], "Token:", token[:10] + "...")

    # 2. Duplicate registration should fail
    print("\n2. Testing Duplicate Register (should be rejected)...")
    try:
        request_json("/api/auth/register", "POST", reg_payload)
        raise AssertionError("Duplicate registration should have failed!")
    except urllib.error.HTTPError as e:
        err_res = json.loads(e.read().decode('utf-8'))
        assert err_res["success"] is False
        print("[OK] Correctly rejected duplicate user:", err_res["error"])

    # 3. Login with credentials
    print("\n3. Testing Login...")
    status, login_res = request_json("/api/auth/login", "POST", {
        "username": "sky_fan_01",
        "password": "mypassword123"
    })
    assert status == 200
    assert login_res["success"] is True
    assert login_res["user"]["avatar"] == "cyber-crown"
    login_token = login_res["token"]
    print("[OK] Login successful! Stored favorites:", login_res["favorites"])

    # 4. Fetch profile with token
    print("\n4. Testing /api/user/profile...")
    status, prof_res = request_json("/api/user/profile", "GET", token=login_token)
    assert status == 200
    assert prof_res["user"]["displayName"] == "Sky Premier VIP"
    assert "sky-atlantic-uk" in prof_res["favorites"]
    print("[OK] Profile fetched:", prof_res["user"]["displayName"], "Favorites count:", len(prof_res["favorites"]))

    # 5. Toggle / save favorites
    print("\n5. Testing /api/user/favorites toggle...")
    status, fav_res = request_json("/api/user/favorites", "POST", {
        "action": "toggle",
        "channelId": "bbc-one-uk"
    }, token=login_token)
    assert status == 200
    assert fav_res["added"] is True
    assert "bbc-one-uk" in fav_res["favorites"]
    print("[OK] Added bbc-one-uk to stored favorites! New list:", fav_res["favorites"])

    # 6. Sync / merge local favorites
    print("\n6. Testing /api/user/favorites/sync...")
    status, sync_res = request_json("/api/user/favorites/sync", "POST", {
        "localFavorites": ["itv1-uk", "film4-uk"]
    }, token=login_token)
    assert status == 200
    assert "itv1-uk" in sync_res["favorites"]
    assert "film4-uk" in sync_res["favorites"]
    print("[OK] Merged local favorites into cloud account! Total count:", len(sync_res["favorites"]))

    # 7. Add recent channel
    print("\n7. Testing /api/user/recent...")
    status, rec_res = request_json("/api/user/recent", "POST", {
        "channelId": "sky-sports-premier-league-uk"
    }, token=login_token)
    assert status == 200
    assert "sky-sports-premier-league-uk" in rec_res["recent"]
    print("[OK] Recent channel saved:", rec_res["recent"])

    # 8. Channel watch stats tracking
    print("\n8. Testing /api/user/stats...")
    status, stat_res = request_json("/api/user/stats", "POST", {
        "channelId": "sky-atlantic-uk",
        "clicks": 1,
        "seconds": 45
    }, token=login_token)
    assert status == 200
    print("[OK] Watch duration and view stats recorded!")

    # 9. Logout
    print("\n9. Testing /api/auth/logout...")
    status, logout_res = request_json("/api/auth/logout", "POST", {
        "token": login_token
    })
    assert status == 200
    print("[OK] Logged out successfully!")

    # 10. Verify revoked token returns 401
    print("\n10. Testing profile with revoked token (should be 401)...")
    try:
        request_json("/api/user/profile", "GET", token=login_token)
        raise AssertionError("Revoked token should have failed with 401!")
    except urllib.error.HTTPError as e:
        assert e.code == 401
        print("[OK] Token correctly revoked!")

    # Clean up test user
    import user_db
    with user_db.get_connection() as conn:
        conn.execute("DELETE FROM users WHERE username = ?", ("sky_fan_01",))
        conn.commit()

    print("\n=== ALL TESTS PASSED SUCCESSFULLY! User accounts & stored favorites operational. ===")

if __name__ == "__main__":
    run_tests()
