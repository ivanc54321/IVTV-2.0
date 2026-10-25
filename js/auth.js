/* ==========================================================================
   IVTV AUTHENTICATION & USER ACCOUNTS MANAGER
   Zero-dependency local & network auth client for IVTV
   ========================================================================== */

const IVTV_AUTH_KEYS = {
  TOKEN: 'ivtv_auth_token_v1',
  USER_CACHE: 'ivtv_user_cache_v1'
};

const IVTV_AVATARS = [
  { id: 'neon-star', icon: '★', label: 'Neon Star', bg: 'linear-gradient(135deg, #00ff88, #00b359)' },
  { id: 'cyber-crown', icon: '👑', label: 'Crown VIP', bg: 'linear-gradient(135deg, #fbbf24, #d97706)' },
  { id: 'cinema-reel', icon: '🎬', label: 'Cinema Reel', bg: 'linear-gradient(135deg, #f43f5e, #be123c)' },
  { id: 'sky-diamond', icon: '💎', label: 'Diamond HD', bg: 'linear-gradient(135deg, #38bdf8, #0284c7)' },
  { id: 'retro-tv', icon: '📺', label: 'Retro TV', bg: 'linear-gradient(135deg, #a855f7, #7e22ce)' },
  { id: 'fire-stream', icon: '🔥', label: 'Fire Streamer', bg: 'linear-gradient(135deg, #f97316, #c2410c)' },
  { id: 'rocket-speed', icon: '🚀', label: 'Turbo HD', bg: 'linear-gradient(135deg, #06b6d4, #0891b2)' },
  { id: 'shield-pro', icon: '🛡️', label: 'Guardian', bg: 'linear-gradient(135deg, #10b981, #047857)' }
];

class AuthManager {
  constructor() {
    this.token = this.loadToken();
    this.user = this.loadCachedUser();
    this.initialized = false;
  }

  loadToken() {
    try {
      return localStorage.getItem(IVTV_AUTH_KEYS.TOKEN) || null;
    } catch (e) {
      return null;
    }
  }

  loadCachedUser() {
    try {
      const data = localStorage.getItem(IVTV_AUTH_KEYS.USER_CACHE);
      return data ? JSON.parse(data) : null;
    } catch (e) {
      return null;
    }
  }

  saveSession(token, user) {
    this.token = token;
    this.user = user;
    try {
      if (token) {
        localStorage.setItem(IVTV_AUTH_KEYS.TOKEN, token);
      } else {
        localStorage.removeItem(IVTV_AUTH_KEYS.TOKEN);
      }
      if (user) {
        localStorage.setItem(IVTV_AUTH_KEYS.USER_CACHE, JSON.stringify(user));
      } else {
        localStorage.removeItem(IVTV_AUTH_KEYS.USER_CACHE);
      }
    } catch (e) {
      console.warn('[Auth] Storage save error:', e);
    }
  }

  getHeaders() {
    const headers = { 'Content-Type': 'application/json' };
    if (this.token) {
      headers['Authorization'] = `Bearer ${this.token}`;
    }
    return headers;
  }

  isLoggedIn() {
    return Boolean(this.token && this.user);
  }

  getUser() {
    return this.user;
  }

  getAvatarMeta(avatarId) {
    const found = IVTV_AVATARS.find(a => a.id === avatarId);
    return found || IVTV_AVATARS[0];
  }

  async init() {
    if (this.initialized) return;
    this.initialized = true;

    if (!this.token) {
      this.dispatchState(false);
      return;
    }

    try {
      const res = await fetch('/api/user/profile', {
        headers: this.getHeaders()
      });

      if (res.ok) {
        const data = await res.json();
        if (data.success && data.user) {
          this.user = data.user;
          this.saveSession(this.token, data.user);
          this.dispatchState(true, {
            favorites: data.favorites || [],
            recent: data.recent || [],
            stats: data.stats || {}
          });
          return;
        }
      }
      // If unauthorized or token invalid, clear
      await this.logout(false);
    } catch (e) {
      console.warn('[Auth] Verification failed, offline or server down, using cached profile:', e);
      if (this.user) {
        this.dispatchState(true);
      } else {
        this.dispatchState(false);
      }
    }
  }

  dispatchState(loggedIn, extra = {}) {
    window.dispatchEvent(new CustomEvent('ivtv:auth-state-changed', {
      detail: {
        loggedIn,
        user: this.user,
        ...extra
      }
    }));
  }

  async register(username, password, displayName = '', avatar = 'neon-star', initialFavorites = []) {
    try {
      const res = await fetch('/api/auth/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          username,
          password,
          displayName,
          avatar,
          initialFavorites
        })
      });

      const data = await res.json();
      if (!res.ok || !data.success) {
        throw new Error(data.error || 'Registration failed');
      }

      this.saveSession(data.token, data.user);
      this.dispatchState(true, {
        favorites: data.favorites || [],
        recent: []
      });

      return data;
    } catch (err) {
      console.error('[Auth] Register error:', err);
      throw err;
    }
  }

  async login(username, password) {
    try {
      const res = await fetch('/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
      });

      const data = await res.json();
      if (!res.ok || !data.success) {
        throw new Error(data.error || 'Login failed');
      }

      this.saveSession(data.token, data.user);
      this.dispatchState(true, {
        favorites: data.favorites || [],
        recent: data.recent || []
      });

      return data;
    } catch (err) {
      console.error('[Auth] Login error:', err);
      throw err;
    }
  }

  async logout(callServer = true) {
    const curToken = this.token;
    this.saveSession(null, null);
    this.dispatchState(false);

    if (callServer && curToken) {
      try {
        await fetch('/api/auth/logout', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ token: curToken })
        });
      } catch (e) {
        // Ignore network errors on logout
      }
    }
  }

  async updateProfile({ displayName, avatar, newPassword }) {
    if (!this.token) throw new Error('Not logged in');

    const res = await fetch('/api/user/profile', {
      method: 'POST',
      headers: this.getHeaders(),
      body: JSON.stringify({ displayName, avatar, newPassword })
    });

    const data = await res.json();
    if (!res.ok || !data.success) {
      throw new Error(data.error || 'Failed to update profile');
    }

    this.user = data.user;
    this.saveSession(this.token, data.user);
    this.dispatchState(true);
    return data.user;
  }
}

// Global Auth Instance
window.IVTV_AVATARS = IVTV_AVATARS;
window.ivtvAuth = new AuthManager();

/* ==========================================================================
   ACCOUNT & AUTH MODAL UI CONTROLLER
   ========================================================================== */

class AccountUI {
  constructor(auth) {
    this.auth = auth;
    this.selectedAvatar = 'neon-star';
    this.overlay = null;
    this.initialized = false;
  }

  init() {
    if (this.initialized) return;
    this.initialized = true;

    this.overlay = document.getElementById('account-modal-overlay');
    if (!this.overlay) return;

    this.renderAvatarGrid();
    this.bindEvents();
    this.bindAuthState();

    // Check initial state
    if (this.auth.isLoggedIn()) {
      this.updateUI(true, this.auth.getUser());
    } else {
      this.updateUI(false, null);
    }
  }

  bindEvents() {
    // Open Modal Triggers
    const openBtn = document.getElementById('nav-account-btn');
    if (openBtn) {
      openBtn.addEventListener('click', () => this.openModal());
    }

    const burgerBtn = document.getElementById('nav-burger-account-btn');
    if (burgerBtn) {
      burgerBtn.addEventListener('click', () => {
        // Close burger dropdown
        const burgerWrapper = document.getElementById('nav-burger-wrapper');
        burgerWrapper?.classList.remove('open');
        this.openModal();
      });
    }

    // Close Modal Triggers
    const closeBtn = document.getElementById('account-modal-close-btn');
    if (closeBtn) {
      closeBtn.addEventListener('click', () => this.closeModal());
    }

    this.overlay?.addEventListener('click', (e) => {
      if (e.target === this.overlay) {
        this.closeModal();
      }
    });

    window.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && this.overlay?.classList.contains('active')) {
        this.closeModal();
      }
    });

    // Tab Switching
    const tabSignin = document.getElementById('tab-btn-signin');
    const tabRegister = document.getElementById('tab-btn-register');
    const formSignin = document.getElementById('form-signin');
    const formRegister = document.getElementById('form-register');

    tabSignin?.addEventListener('click', () => {
      tabSignin.classList.add('active');
      tabRegister?.classList.remove('active');
      if (formSignin) formSignin.style.display = 'flex';
      if (formRegister) formRegister.style.display = 'none';
      this.clearError();
    });

    tabRegister?.addEventListener('click', () => {
      tabRegister.classList.add('active');
      tabSignin?.classList.remove('active');
      if (formRegister) formRegister.style.display = 'flex';
      if (formSignin) formSignin.style.display = 'none';
      this.clearError();
    });

    // Password Toggles
    this.bindPasswordToggle('toggle-signin-password', 'signin-password');
    this.bindPasswordToggle('toggle-register-password', 'register-password');

    // Sign In Submit
    formSignin?.addEventListener('submit', async (e) => {
      e.preventDefault();
      const usernameInput = document.getElementById('signin-username');
      const passwordInput = document.getElementById('signin-password');
      const submitBtn = document.getElementById('btn-submit-signin');

      const username = usernameInput?.value.trim();
      const password = passwordInput?.value;

      if (!username || !password) {
        this.showError('Please enter both username and password.');
        return;
      }

      this.setButtonLoading(submitBtn, true, 'Signing In...');
      this.clearError();

      try {
        const res = await this.auth.login(username, password);
        this.setButtonLoading(submitBtn, false, 'Sign In & Load Favorites');
        if (window.showToast) {
          window.showToast(`Welcome back, ${res.user.displayName || res.user.username}!`, 'success');
        }
        passwordInput.value = '';
        this.switchToDashboard();
      } catch (err) {
        this.setButtonLoading(submitBtn, false, 'Sign In & Load Favorites');
        this.showError(err.message || 'Login failed. Please check your credentials.');
      }
    });

    // Register Submit
    formRegister?.addEventListener('submit', async (e) => {
      e.preventDefault();
      const displayInput = document.getElementById('register-displayname');
      const usernameInput = document.getElementById('register-username');
      const passwordInput = document.getElementById('register-password');
      const importCheckbox = document.getElementById('register-import-favs');
      const submitBtn = document.getElementById('btn-submit-register');

      const username = usernameInput?.value.trim();
      const password = passwordInput?.value;
      const displayName = displayInput?.value.trim() || username;
      const shouldImport = importCheckbox?.checked ?? true;

      if (!username || !password) {
        this.showError('Username and password are required.');
        return;
      }

      if (password.length < 4) {
        this.showError('Password must be at least 4 characters.');
        return;
      }

      const initialFavs = shouldImport && window.ivtvStorage ? window.ivtvStorage.getFavorites() : [];

      this.setButtonLoading(submitBtn, true, 'Creating Account...');
      this.clearError();

      try {
        const res = await this.auth.register(
          username, password, displayName, this.selectedAvatar, initialFavs
        );
        this.setButtonLoading(submitBtn, false, 'Create Account & Sync');
        if (window.showToast) {
          window.showToast(`Welcome to IVTV, ${res.user.displayName || res.user.username}!`, 'success');
        }
        passwordInput.value = '';
        this.switchToDashboard();
      } catch (err) {
        this.setButtonLoading(submitBtn, false, 'Create Account & Sync');
        this.showError(err.message || 'Registration failed.');
      }
    });

    // Logout Button
    const logoutBtn = document.getElementById('dash-logout-btn');
    if (logoutBtn) {
      logoutBtn.addEventListener('click', async () => {
        if (confirm('Are you sure you want to sign out? Your stored favorites remain safely in your account.')) {
          await this.auth.logout();
          if (window.showToast) {
            window.showToast('Signed out successfully. Switched to Guest mode.', 'info');
          }
          this.switchToAuth();
        }
      });
    }

    // Force Sync Button
    const syncBtn = document.getElementById('dash-force-sync-btn');
    if (syncBtn) {
      syncBtn.addEventListener('click', async () => {
        syncBtn.textContent = 'Syncing...';
        syncBtn.style.opacity = '0.7';
        if (window.ivtvStorage) {
          await window.ivtvStorage.syncWithServer();
        }
        setTimeout(() => {
          syncBtn.textContent = 'Synced ✓';
          syncBtn.style.opacity = '1';
          if (window.showToast) {
            window.showToast('Favorites and watch history synced to cloud!', 'success');
          }
          this.renderDashboardFavorites();
          setTimeout(() => {
            syncBtn.textContent = 'Force Sync';
          }, 2000);
        }, 500);
      });
    }

    // Listen to favorite change events to keep dashboard updated in real-time
    window.addEventListener('ivtv:favorites-changed', () => {
      if (this.overlay?.classList.contains('active') && this.auth.isLoggedIn()) {
        this.renderDashboardFavorites();
      }
    });
  }

  bindPasswordToggle(btnId, inputId) {
    const btn = document.getElementById(btnId);
    const input = document.getElementById(inputId);
    if (!btn || !input) return;
    btn.addEventListener('click', () => {
      if (input.type === 'password') {
        input.type = 'text';
        btn.textContent = '🙈';
      } else {
        input.type = 'password';
        btn.textContent = '👁';
      }
    });
  }

  bindAuthState() {
    window.addEventListener('ivtv:auth-state-changed', (e) => {
      const { loggedIn, user } = e.detail || {};
      this.updateUI(loggedIn, user);
    });
  }

  renderAvatarGrid() {
    const grid = document.getElementById('avatar-grid');
    if (!grid) return;
    grid.innerHTML = '';

    IVTV_AVATARS.forEach((av) => {
      const opt = document.createElement('div');
      opt.className = `avatar-option ${av.id === this.selectedAvatar ? 'selected' : ''}`;
      opt.dataset.avatarId = av.id;
      opt.innerHTML = `
        <div class="avatar-bubble" style="background: ${av.bg};">${av.icon}</div>
        <span class="avatar-name">${av.label}</span>
      `;
      opt.addEventListener('click', () => {
        this.selectedAvatar = av.id;
        grid.querySelectorAll('.avatar-option').forEach(el => el.classList.remove('selected'));
        opt.classList.add('selected');
      });
      grid.appendChild(opt);
    });
  }

  updateUI(loggedIn, user) {
    const navBtn = document.getElementById('nav-account-btn');
    const navLabel = document.getElementById('nav-account-label');
    const navAvatar = document.getElementById('nav-account-avatar');
    const burgerLabel = document.getElementById('burger-account-label');
    const burgerHint = document.getElementById('burger-account-hint');

    if (loggedIn && user) {
      const avMeta = this.auth.getAvatarMeta(user.avatar);
      if (navBtn) navBtn.classList.add('logged-in');
      if (navLabel) navLabel.textContent = user.displayName || user.username;
      if (navAvatar) {
        navAvatar.innerHTML = `<span style="font-size: 0.8rem;">${avMeta.icon}</span>`;
        navAvatar.style.background = avMeta.bg;
        navAvatar.style.color = '#ffffff';
      }
      if (burgerLabel) burgerLabel.textContent = user.displayName || user.username;
      if (burgerHint) burgerHint.textContent = 'Active Account • VIP Member';

      this.populateDashboard(user);
    } else {
      if (navBtn) navBtn.classList.remove('logged-in');
      if (navLabel) navLabel.textContent = 'Sign In';
      if (navAvatar) {
        navAvatar.innerHTML = `
          <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
            <circle cx="12" cy="7" r="4"/>
          </svg>
        `;
        navAvatar.style.background = 'rgba(0, 255, 136, 0.18)';
        navAvatar.style.color = 'var(--accent-neon)';
      }
      if (burgerLabel) burgerLabel.textContent = 'Account & Cloud Sync';
      if (burgerHint) burgerHint.textContent = 'Sign In / Stored Favorites';
    }
  }

  populateDashboard(user) {
    const avMeta = this.auth.getAvatarMeta(user.avatar);
    const dashBadge = document.getElementById('dash-avatar-badge');
    const dashIcon = document.getElementById('dash-avatar-icon');
    const dashName = document.getElementById('dash-display-name');
    const dashUser = document.getElementById('dash-username');

    if (dashBadge) dashBadge.style.background = avMeta.bg;
    if (dashIcon) dashIcon.textContent = avMeta.icon;
    if (dashName) dashName.textContent = user.displayName || user.username;
    if (dashUser) dashUser.textContent = `@${user.username}`;

    this.renderDashboardFavorites();
  }

  renderDashboardFavorites() {
    const list = document.getElementById('dash-favorites-list');
    const favCount = document.getElementById('dash-favs-count');
    const recentCount = document.getElementById('dash-recent-count');
    if (!list) return;

    const favIds = window.ivtvStorage ? window.ivtvStorage.getFavorites() : [];
    const recentIds = window.ivtvStorage ? window.ivtvStorage.getRecent() : [];

    if (favCount) favCount.textContent = favIds.length;
    if (recentCount) recentCount.textContent = recentIds.length;

    list.innerHTML = '';

    if (favIds.length === 0) {
      list.innerHTML = `
        <div class="account-fav-empty">
          You don't have any saved favorites yet.<br>Click the ★ star on any channel to save it to your account!
        </div>
      `;
      return;
    }

    const allChannels = (window.IVTV_DATA && Array.isArray(window.IVTV_DATA.channels)) ? window.IVTV_DATA.channels : [];

    favIds.forEach(id => {
      const ch = allChannels.find(c => c.id === id) || {
        id,
        name: id.replace(/-/g, ' ').replace(/\b\w/g, l => l.toUpperCase()),
        logo: 'assets/icon-192.png',
        category: 'TV Channel'
      };

      const item = document.createElement('div');
      item.className = 'account-fav-item';
      item.innerHTML = `
        <div class="account-fav-info">
          <img src="${ch.logo}" alt="${ch.name}" class="account-fav-logo" onerror="this.src='assets/icon-192.png'">
          <div>
            <div class="account-fav-name">${ch.name}</div>
            <div class="account-fav-category">${ch.category || 'Live TV'}</div>
          </div>
        </div>
        <div class="account-fav-actions">
          <button type="button" class="account-fav-play-btn" data-play-id="${ch.id}" title="Watch ${ch.name}">
            <svg width="12" height="12" viewBox="0 0 24 24"><polygon points="5 3 19 12 5 21 5 3"/></svg>
            <span>Play</span>
          </button>
          <button type="button" class="account-fav-remove-btn" data-remove-id="${ch.id}" title="Remove from favorites">
            ✕
          </button>
        </div>
      `;

      item.querySelector('[data-play-id]')?.addEventListener('click', () => {
        this.closeModal();
        if (window.ivtvPlayer) {
          window.ivtvPlayer.openPlayer(ch.id);
        }
      });

      item.querySelector('[data-remove-id]')?.addEventListener('click', () => {
        if (window.ivtvStorage) {
          window.ivtvStorage.toggleFavorite(ch.id);
          this.renderDashboardFavorites();
        }
      });

      list.appendChild(item);
    });
  }

  switchToDashboard() {
    const authView = document.getElementById('account-auth-view');
    const dashView = document.getElementById('account-dashboard-view');
    const headerTitle = document.getElementById('account-modal-title');
    const headerSub = document.getElementById('account-modal-subtitle');

    if (authView) authView.style.display = 'none';
    if (dashView) dashView.style.display = 'block';
    if (headerTitle) headerTitle.textContent = 'Account Dashboard';
    if (headerSub) headerSub.textContent = 'Your cloud-synced profile & stored favorites';

    if (this.auth.getUser()) {
      this.populateDashboard(this.auth.getUser());
    }
  }

  switchToAuth() {
    const authView = document.getElementById('account-auth-view');
    const dashView = document.getElementById('account-dashboard-view');
    const headerTitle = document.getElementById('account-modal-title');
    const headerSub = document.getElementById('account-modal-subtitle');

    if (authView) authView.style.display = 'block';
    if (dashView) dashView.style.display = 'none';
    if (headerTitle) headerTitle.textContent = 'IVTV Account';
    if (headerSub) headerSub.textContent = 'Sync favorites & watch history across all devices';
    this.clearError();
  }

  openModal() {
    if (!this.overlay) return;
    this.overlay.classList.add('active');
    document.body.style.overflow = 'hidden';

    if (this.auth.isLoggedIn()) {
      this.switchToDashboard();
    } else {
      this.switchToAuth();
    }
  }

  closeModal() {
    if (!this.overlay) return;
    this.overlay.classList.remove('active');
    document.body.style.overflow = '';
  }

  showError(msg) {
    const box = document.getElementById('auth-error-box');
    const text = document.getElementById('auth-error-text');
    if (box && text) {
      text.textContent = msg;
      box.style.display = 'flex';
    }
  }

  clearError() {
    const box = document.getElementById('auth-error-box');
    if (box) box.style.display = 'none';
  }

  setButtonLoading(btn, loading, defaultText) {
    if (!btn) return;
    if (loading) {
      btn.disabled = true;
      btn.style.opacity = '0.7';
      btn.innerHTML = `<span>${defaultText}</span>`;
    } else {
      btn.disabled = false;
      btn.style.opacity = '1';
      btn.innerHTML = `
        <span>${defaultText}</span>
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="9 18 15 12 9 6"/></svg>
      `;
    }
  }
}

// Global UI Instance and DOMContentLoaded bootstrap
window.ivtvAccountUI = new AccountUI(window.ivtvAuth);
const initAccountUI = () => {
  try {
    window.ivtvAccountUI.init();
  } catch (err) {
    console.warn('[AccountUI] Safe init caught error:', err);
  }
};

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initAccountUI);
} else {
  initAccountUI();
}

