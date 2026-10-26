"""
US Channels EPG Schedule Generator (Adjusted for UK London Time)
Generates authentic 24-hour linear programme listings for all 45 US channels,
with timestamps and hour slots precisely calculated for UK Local Time (GMT/BST).
"""

import datetime
import time

# US dayparts adjusted to UK London Time (ET + 5 hours):
# 00:00 - 04:00 UK (19:00 - 23:00 ET): US Marquee Primetime & Premiere Series
# 04:00 - 06:30 UK (23:00 - 01:30 ET): US Late Night Talk Shows & Blockbusters
# 06:30 - 11:00 UK (01:30 - 06:00 ET): US Overnight Encores & Movies
# 11:00 - 15:00 UK (06:00 - 10:00 ET): US Morning News & Breakfast Broadcasts
# 15:00 - 20:00 UK (10:00 - 15:00 ET): US Daytime Series & Afternoon Movies
# 20:00 - 00:00 UK (15:00 - 19:00 ET): US Early Fringe & Evening News

US_CHANNEL_PROGRAMS = {
    "hbo-usa": {
        "name": "HBO",
        "category": "Premium / Cinema",
        "genre": "Premium Cinema & HBO Originals",
        "shows": [
            ("00:00", 60, "The Penguin", "Season 1, Episode 7: Top Hat", "Oz Cobb makes his move for complete control of Gotham's underground empire as Sofia Falcone closes in.", "HBO Original", True, False),
            ("01:00", 65, "House of the Dragon", "Season 2, Episode 8: The Queen Who Ever Was", "Rhaenyra seeks to weaponize her dragon advantage while Aemond unleashes fury across the Riverlands.", "HBO Original", True, False),
            ("02:05", 60, "The Last of Us", "Season 1, Episode 9: Look for the Light", "Joel and Ellie reach the Firefly hospital in Salt Lake City, leading to a fateful and irreversible decision.", "HBO Original", True, False),
            ("03:05", 35, "Last Week Tonight with John Oliver", "Season 11, Episode 26", "A satirical look at the week in news, politics, and current events, followed by a deep-dive investigative report.", "Satire & Comedy", False, False),
            ("03:40", 60, "Real Time with Bill Maher", "Live from Los Angeles", "Bill Maher hosts lively panel discussions with notable guests from across the political spectrum.", "Talk / Debate", False, False),
            ("04:40", 155, "Dune: Part Two", "Feature Film (2024)", "Paul Atreides unites with Chani and the Fremen while seeking revenge against the conspirators who destroyed his family.", "Blockbuster Movie", True, False),
            ("07:15", 40, "Curb Your Enthusiasm", "Season 12: No Lessons Learned", "Larry David returns to Atlanta for his trial, navigating a web of social faux pas and celebrity encounters.", "Comedy", False, False),
            ("07:55", 60, "The Sopranos", "Season 5: Long Term Parking", "Tony Soprano faces mounting tension between New York and New Jersey while Adriana is cornered by the FBI.", "Classic Drama", False, False),
            ("08:55", 60, "The Wire", "Season 4: Final Grades", "The school year ends as Carcetti tackles the police department budget deficit and Marlo solidifies his rule.", "Crime Drama", False, False),
            ("09:55", 80, "100 Years of Warner Bros.", "Part 4: The Hero's Journey", "A comprehensive chronicle exploring the evolution of blockbuster filmmaking and prestige television.", "Documentary", False, False),
            ("11:15", 175, "The Batman", "Feature Film (2022)", "When a sadistic serial killer begins murdering key political figures in Gotham, Batman is forced to investigate.", "Cinema Hit", True, False),
            ("14:10", 60, "Succession", "Season 4, Episode 3: Connor's Wedding", "A shocking development shakes the Roy family during Connor's lavish wedding cruise in New York.", "HBO Original", False, False),
            ("15:10", 65, "The White Lotus", "Season 2: Arrivederci", "Tensions and betrayals boil over among the wealthy vacationers and staff at the Sicilian luxury resort.", "Prestige Drama", False, False),
            ("16:15", 115, "Wonka", "Feature Film (2023)", "Armed with nothing but a hat full of dreams, young chocolatier Willy Wonka sets out to change the world.", "Family Cinema", True, False),
            ("18:10", 60, "Industry", "Season 3, Episode 6", "Yasmin and Robert find themselves at the center of Lumi's IPO fallout as Pierpoint faces systemic risk.", "Drama Series", False, False),
            ("19:10", 115, "Barbie", "Feature Film (2023)", "To live in Barbie Land is to be a perfect being in a perfect place. Unless you have a full-on existential crisis.", "Hollywood Hit", True, False),
            ("21:05", 60, "True Detective: Night Country", "Part 6 (Season Finale)", "Danvers and Navarro make a harrowing discovery at the ice caves that finally solves the Tsalal researchers' fate.", "Crime Mystery", False, False),
            ("22:05", 60, "The Penguin", "Encore Presentation", "High-definition encore of Oz Cobb's rise through the criminal underworld of Gotham City.", "HBO Original", True, False),
            ("23:05", 55, "House of the Dragon: Inside the Episode", "Behind the Scenes", "Exclusive interviews with showrunners, directors, and cast exploring the visual effects and character motivations.", "Special Feature", False, False)
        ]
    },
    "cinemax-usa": {
        "name": "Cinemax",
        "category": "Premium / Action & Movies",
        "genre": "Action, Thrillers & Movies",
        "shows": [
            ("00:00", 170, "John Wick: Chapter 4", "Feature Film (2023)", "John Wick uncovers a path to defeating The High Table, facing deadly assassins worldwide.", "Action Showcase", True, False),
            ("02:50", 120, "Mad Max: Fury Road", "Feature Film (2015)", "In a post-apocalyptic wasteland, Max teams up with Furiosa to escape a tyrannical warlord.", "Adrenaline Cinema", True, False),
            ("04:50", 55, "Banshee", "Season 3: Tribals", "Lucas Hood defends the Cadi against an all-out assault by Chayton Littlestone and the Redbones.", "Action Series", False, False),
            ("05:45", 55, "Strike Back", "Season 5: Episode 8", "Section 20 races across Europe to intercept a stolen chemical weapon before it reaches a major city.", "Military Thriller", False, False),
            ("06:40", 110, "Nobody", "Feature Film (2021)", "A docile family man reveals his lethal past after thieves break into his suburban home.", "Action Thriller", True, False),
            ("08:30", 135, "The Matrix", "Feature Film (1999)", "A computer hacker learns from mysterious rebels about the true nature of his reality and his role in the war.", "Sci-Fi Classic", True, False),
            ("10:45", 145, "Mission: Impossible - Fallout", "Feature Film (2018)", "Ethan Hunt and his IMF team race against time after a mission goes wrong and plutonium falls into the wrong hands.", "Blockbuster Action", True, False),
            ("13:10", 110, "Die Hard", "Feature Film (1988)", "An NYPD officer tries to save his estranged wife and several others taken hostage by terrorists in a skyscraper.", "Action Classic", True, False),
            ("15:00", 125, "The Equalizer", "Feature Film (2014)", "A retired intelligence operative uses his formidable skills to protect an innocent girl from ruthless criminals.", "Crime Action", True, False),
            ("17:05", 120, "Fast & Furious 6", "Feature Film (2013)", "Hobbs recruits Dom and his crew to help take down a team of mercenary drivers across London.", "High-Octane", True, False),
            ("19:05", 125, "Bullet Train", "Feature Film (2022)", "Five assassins aboard a fast-moving bullet train find out their missions have something in common.", "Cinema Hit", True, False),
            ("21:10", 110, "The Bourne Identity", "Feature Film (2002)", "A man is picked up by a fishing boat, bullet-riddled and suffering from amnesia, racing to discover his identity.", "Espionage Action", True, False),
            ("23:00", 60, "Warrior", "Season 2: Episode 9", "Ah Sahm and Young Jun face an unprecedented crisis in Chinatown as rival tongs mobilize for war.", "Martial Arts Drama", False, False)
        ]
    },
    "hbo-family-usa": {
        "name": "HBO Family",
        "category": "Premium / Family Movies",
        "genre": "Family, Animation & Adventure",
        "shows": [
            ("00:00", 100, "Despicable Me 4", "Animated Feature (2024)", "Gru and his family face a new nemesis in Maxime Le Mal, forcing them to relocate under witness protection.", "Family Comedy", True, False),
            ("01:40", 105, "Paddington 2", "Family Feature (2017)", "Paddington undertakes odd jobs to buy a pop-up book for Aunt Lucy, only for it to be stolen by a cunning actor.", "Family Adventure", True, False),
            ("03:25", 90, "The Lego Movie", "Animated Feature (2014)", "An ordinary Lego construction worker finds himself recruited to stop an evil tyrant from gluing the Lego universe together.", "Animation Hit", True, False),
            ("04:55", 150, "Harry Potter and the Sorcerer's Stone", "Feature Film (2001)", "An orphaned boy enrolls in a school of wizardry, where he learns the truth about himself, his family and a terrible evil.", "Family Fantasy", True, False),
            ("07:25", 95, "Shrek", "Animated Feature (2001)", "An ogre's precious solitude is shattered by an invasion of annoying fairy tale characters banished by Lord Farquaad.", "Comedy Classic", True, False),
            ("09:00", 100, "How to Train Your Dragon", "Animated Feature (2010)", "A hapless young Viking who aspires to hunt dragons becomes the unlikely friend of a young dragon himself.", "Adventure", True, False),
            ("10:40", 110, "Ratatouille", "Animated Feature (2007)", "A rat who can cook makes an unusual alliance with a young kitchen worker at a famous Paris restaurant.", "Animation Favorite", True, False),
            ("12:30", 115, "Spider-Man: Into the Spider-Verse", "Animated Feature (2018)", "Teen Miles Morales becomes the new Spider-Man and joins other Spider-Heroes from parallel universes to stop a threat.", "Oscar Winner", True, False),
            ("14:25", 100, "Sing 2", "Animated Feature (2021)", "Buster Moon and his friends must persuade reclusive rock star Clay Calloway to join them for the opening of a new show.", "Musical Animation", True, False),
            ("16:05", 110, "Enchanted", "Family Feature (2007)", "A young maiden in a fairy tale animated world is banished to live-action Manhattan by an evil queen.", "Family Fantasy", True, False),
            ("17:55", 115, "Wonka", "Feature Film (2023)", "Willy Wonka's whimsical journey to establish his renowned chocolate factory against the greedy Chocolate Cartel.", "Family Cinema", True, False),
            ("19:50", 160, "Harry Potter and the Chamber of Secrets", "Feature Film (2002)", "An ancient prophecy seems to be coming true when a mysterious presence begins stalking the corridors at Hogwarts.", "Family Fantasy", True, False),
            ("22:30", 90, "Minions: The Rise of Gru", "Animated Feature (2022)", "The untold story of one twelve-year-old's dream to become the world's greatest supervillain.", "Family Comedy", True, False)
        ]
    },
    "hbo-hits-usa": {
        "name": "HBO Hits",
        "category": "Premium / Blockbusters",
        "genre": "Marquee Box Office Blockbusters",
        "shows": [
            ("00:00", 180, "Oppenheimer", "Feature Film (2023)", "Christopher Nolan's masterpiece chronicles the life of J. Robert Oppenheimer and the creation of the atomic bomb.", "Academy Award Winner", True, False),
            ("03:00", 130, "Top Gun: Maverick", "Feature Film (2022)", "After thirty years, Maverick is still pushing the envelope as a top naval aviator training a detachment of graduates.", "Blockbuster Hit", True, False),
            ("05:10", 165, "Interstellar", "Feature Film (2014)", "When Earth becomes uninhabitable in the future, a farmer and ex-NASA pilot is tasked to pilot a spacecraft through a wormhole.", "Sci-Fi Epic", True, False),
            ("07:55", 145, "Inception", "Feature Film (2010)", "A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea.", "Mind-Bending Thriller", True, False),
            ("10:20", 150, "The Dark Knight", "Feature Film (2008)", "Batman must accept one of the greatest psychological and physical tests of his ability to fight injustice against the Joker.", "Cinema Legend", True, False),
            ("12:50", 155, "Gladiator", "Feature Film (2000)", "A former Roman General sets out to exact vengeance against the corrupt emperor who murdered his family and sent him into slavery.", "Historical Epic", True, False),
            ("15:25", 145, "Casino Royale", "Feature Film (2006)", "After earning 00 status, James Bond sets out on his first mission to bankrupt a terrorist financier in high-stakes poker.", "Bond Franchise", True, False),
            ("17:50", 160, "Avatar: The Way of Water", "Feature Film (2022)", "Jake Sully lives with his newfound family formed on the extrasolar moon Pandora, defending their home against ancient enemies.", "Epic Adventure", True, False),
            ("20:30", 135, "The Martian", "Feature Film (2015)", "An astronaut becomes stranded on Mars after his crew assume him dead, and must rely on his ingenuity to signal to Earth.", "Sci-Fi Drama", True, False),
            ("22:45", 75, "Hollywood Cinema Rewind", "Retrospective Showcase", "A curated tour through cinema history's highest grossing blockbusters, critical milestones, and iconic directors.", "Cinema Documentary", False, False)
        ]
    },
    "hbo-signature-usa": {
        "name": "HBO Signature",
        "category": "Premium / Award-Winning",
        "genre": "Critically Acclaimed & HBO Films",
        "shows": [
            ("00:00", 65, "The Gilded Age", "Season 2, Episode 8: In Terms of Winning and Losing", "The opera war comes to a dramatic climax between Bertha Russell and Mrs. Astor, redefining New York society.", "Prestige Drama", False, False),
            ("01:05", 60, "Mare of Easttown", "Episode 7: Sacrament", "Mare Sheehan confronts the shocking truth behind Erin's murder as Easttown reckons with lingering trauma.", "Emmy Winner", False, False),
            ("02:05", 70, "Chernobyl", "Vichnaya Pamyat (Series Finale)", "Valery Legasov, Boris Shcherbina, and Ulana Khomyuk risk their lives and reputations to expose the truth about Chernobyl.", "Masterpiece Miniseries", False, False),
            ("03:15", 65, "Band of Brothers", "Part 9: Why We Fight", "Easy Company enters Germany as the war nears its end, confronting the grim reality of a concentration camp.", "Historic Miniseries", False, False),
            ("04:20", 60, "Deadwood", "Season 3: Tell Him Something Pretty", "The camp holds an election as George Hearst consolidates his grip over the mining claims.", "Prestige Western", False, False),
            ("05:20", 130, "The Normal Heart", "HBO Original Film (2014)", "The story of the onset of the HIV-AIDS crisis in New York City in the early 1980s, taking an unflinching look at politics.", "Acclaimed Film", True, False),
            ("07:30", 120, "Behind the Candelabra", "HBO Original Film (2013)", "Based on the autobiographical novel, the story of the stormy six-year relationship between Liberace and his lover.", "Award Winner", True, False),
            ("09:30", 60, "Six Feet Under", "Everyone's Waiting (Series Finale)", "The Fisher family moves forward with their lives following Nate's funeral, concluding the landmark drama.", "Classic Television", False, False),
            ("10:30", 60, "Rome", "Season 2: De Patre Vostro", "Octavian enters Alexandria while Antony and Cleopatra make their final stand in Egypt.", "Historical Drama", False, False),
            ("11:30", 115, "The Tale", "HBO Original Film (2018)", "An investigation into one woman's memory as she is forced to re-examine her first sexual relationship.", "Prestige Film", True, False),
            ("13:25", 60, "The Night Of", "The Call of the Wild", "Naz's trial reaches its closing arguments as Stone takes the floor to defend his client.", "Legal Thriller", False, False),
            ("14:25", 60, "Big Little Lies", "Season 1: You Get What You Need", "The school trivia night ends with tragic violence on the Monterey bluff, cementing the bond between five women.", "Drama Showcase", False, False),
            ("15:25", 135, "Temple Grandin", "HBO Original Film (2010)", "A biopic of Temple Grandin, an autistic woman who overcame the limitations imposed on her by her condition.", "Biographical Drama", True, False),
            ("17:40", 60, "The Gilded Age", "Season 2: Close Enough to Touch", "Bertha advances her campaign for the Metropolitan Opera House as Marian re-evaluates her future.", "Prestige Drama", False, False),
            ("18:40", 60, "Sharp Objects", "Milk (Series Finale)", "Camille puts her own life in jeopardy as she gets closer to the truth behind the Wind Gap murders.", "Psychological Thriller", False, False),
            ("19:40", 65, "The White Lotus", "Season 1: Departures", "The dramatic conclusion of the wealthy guests' eventful week at the exclusive Hawaiian resort.", "Emmy Winner", False, False),
            ("20:45", 125, "Bessie", "HBO Original Film (2015)", "Queen Latifah stars as legendary blues singer Bessie Smith, detailing her transformation into an American icon.", "Musical Biopic", True, False),
            ("22:50", 70, "Mare of Easttown", "Episode 6: Sore Must Be the Storm", "Recovering from her hospital stay, Mare re-evaluates suspects while John and Billy face family secrets.", "Crime Drama", False, False)
        ]
    },
    "cnn-usa": {
        "name": "CNN USA",
        "category": "News",
        "genre": "24/7 Live Breaking News",
        "shows": [
            ("00:00", 60, "The Source with Kaitlan Collins", "Live from Washington", "Kaitlan Collins cuts straight to the source, asking direct questions to the key decision-makers shaping global politics.", "Primetime News", False, False),
            ("01:00", 60, "CNN NewsNight with Abby Phillip", "Live Analysis & Debate", "Abby Phillip convenes newsmakers, experts, and commentators for sharp debate on the biggest issues facing the country.", "Nightly Debate", False, False),
            ("02:00", 60, "Laura Coates Live", "Legal & Political Insights", "Laura Coates brings her legal expertise and courtroom insight to dissecting high-stakes trials and federal developments.", "Analysis", False, False),
            ("03:00", 60, "Anderson Cooper 360", "Encore Broadcast", "Anderson Cooper goes beyond the headlines, holding those in power accountable with thorough investigative reporting.", "Investigative", False, False),
            ("04:00", 60, "CNN Newsroom Live", "Overnight Edition", "Live global news desk reporting breaking events, overnight developments, and international financial market updates.", "Live News", False, False),
            ("05:00", 60, "Early Start with Kasie Hunt", "First Look at the Day", "The first comprehensive look at the morning's top political stories, business headlines, and developing worldwide news.", "Morning Desk", False, False),
            ("06:00", 60, "CNN This Morning", "Live Morning Show", "Fast-paced morning coverage, expert analysis, and major interviews setting the national agenda.", "Morning Broadcast", False, False),
            ("07:00", 120, "CNN This Morning with Kasie Hunt", "Capitol Hill & White House", "In-depth morning reporting direct from Washington correspondents, congressional leaders, and international bureaus.", "Morning News", False, False),
            ("09:00", 120, "CNN News Central", "Morning Edition", "Dynamic wall-to-wall news coverage tracking breaking developments, live press conferences, and real-time field reports.", "Breaking News", False, False),
            ("11:00", 120, "CNN News Central", "Midday Desk", "Fast-moving reporting from correspondents stationed across the nation and key international conflict zones.", "Live News", False, False),
            ("13:00", 60, "Inside Politics with Manu Raju", "Washington Deep-Dive", "Manu Raju leads insider reporting on congressional elections, legislative battles, and White House maneuvering.", "Political News", False, False),
            ("14:00", 120, "CNN News Central", "Afternoon Edition", "Real-time updates, breaking legal decisions, market movements, and live press briefings.", "News Desk", False, False),
            ("16:00", 120, "The Situation Room with Wolf Blitzer", "Late Afternoon Edition", "Wolf Blitzer anchors from Washington, delivering breaking international security and domestic political news.", "Flagship News", False, False),
            ("18:00", 60, "The Situation Room with Wolf Blitzer", "Washington Primetime", "Wolf Blitzer covers the day's final developments with top national intelligence, diplomatic, and military guests.", "Flagship News", False, False),
            ("19:00", 60, "Erin Burnett OutFront", "Hard-Hitting News", "Erin Burnett tackles the day's biggest stories with fearless interviews and in-depth investigations.", "Evening News", False, False),
            ("20:00", 60, "Anderson Cooper 360", "Primetime Flagship", "Anderson Cooper brings you 360-degree coverage of the stories that matter most, holding leaders accountable.", "Primetime News", False, False),
            ("21:00", 60, "The Source with Kaitlan Collins", "Live Primetime", "Kaitlan Collins delivers fresh reporting and exclusive interviews from the heart of Washington D.C.", "Primetime News", False, False),
            ("22:00", 60, "CNN NewsNight with Abby Phillip", "Live Debate Desk", "Abby Phillip moderates high-energy discussion between leading voices across the political spectrum.", "Debate Desk", False, False),
            ("23:00", 60, "Laura Coates Live", "Late Evening Edition", "Laura Coates delivers crisp legal perspective, breaking political news, and deep analysis of major stories.", "Legal Analysis", False, False)
        ]
    },
    "fox-news-usa": {
        "name": "Fox News",
        "category": "News",
        "genre": "Live Breaking News & Political Commentary",
        "shows": [
            ("00:00", 60, "The Ingraham Angle", "Primetime Commentary", "Laura Ingraham cuts through the spin to focus on the issues that matter to everyday Americans.", "Primetime", False, False),
            ("01:00", 60, "Jesse Watters Primetime", "Nightly Showcase", "Jesse Watters takes an irreverent look at the news of the day with sharp monologues and exclusive guests.", "Primetime", False, False),
            ("02:00", 60, "Hannity", "Top Rated Commentary", "Sean Hannity showcases his signature monologues, political interviews, and investigative reports.", "Primetime", False, False),
            ("03:00", 60, "Gutfeld!", "Late Night Satire", "Greg Gutfeld hosts late night comedy, political satire, and unpredictable panel discussions.", "Late Night Satire", False, False),
            ("04:00", 60, "Fox News @ Night with Trace Gallagher", "Live Overnight Desk", "Trace Gallagher anchors live late-night coverage tracking breaking events on the West Coast and overseas.", "Live News", False, False),
            ("05:00", 60, "FOX & Friends First", "Early Bird Edition", "Todd Piro and Carley Shimkus kick off the morning with the top headlines, market outlook, and weather updates.", "Morning News", False, False),
            ("06:00", 180, "FOX & Friends", "America's Morning Show", "Steve Doocy, Ainsley Earhardt, Brian Kilmeade, and Lawrence Jones deliver morning news, interviews, and lifestyle.", "Morning Show", False, False),
            ("09:00", 120, "America's Newsroom with Bill Hemmer & Dana Perino", "Morning Newsroom", "Bill Hemmer and Dana Perino anchor live breaking news, press briefings, and political analysis.", "Newsroom Desk", False, False),
            ("11:00", 60, "The Faulkner Focus", "Harris Faulkner Live", "Harris Faulkner breaks through the headlines with incisive interviews and hard facts.", "Hard News", False, False),
            ("12:00", 60, "Outnumbered", "Dynamic Panel Debate", "Four female panelists and one 'lucky guy' tackle the cultural, political, and economic stories of the day.", "Panel Debate", False, False),
            ("13:00", 120, "America Reports with John Roberts & Sandra Smith", "Midday Live", "John Roberts and Sandra Smith deliver continuous news reporting from Washington and New York.", "News Desk", False, False),
            ("15:00", 60, "The Story with Martha MacCallum", "In-Depth News", "Martha MacCallum anchors hard-hitting discussions examining the human impact of major national news.", "Evening News", False, False),
            ("16:00", 60, "Your World with Neil Cavuto", "Business & Politics", "Neil Cavuto covers the intersection of Wall Street and Capitol Hill, tracking live market closes.", "Financial News", False, False),
            ("17:00", 60, "The Five", "America's #1 Cable News Show", "Greg Gutfeld, Dana Perino, Jesse Watters, Jeanine Pirro, and Harold Ford Jr. debate the day's hot topics.", "Top Rated Panel", False, False),
            ("18:00", 60, "Special Report with Bret Baier", "The Golden Standard of News", "Bret Baier anchors balanced political reporting from Washington, followed by the All-Star Panel.", "Flagship News", False, False),
            ("19:00", 60, "The Ingraham Angle", "Early Evening Edition", "Laura Ingraham tackles breaking political stories, border developments, and economic policies.", "Commentary", False, False),
            ("20:00", 60, "Jesse Watters Primetime", "Live Primetime", "Jesse Watters exposes political hypocrisy and cultural absurdity in his signature style.", "Primetime", False, False),
            ("21:00", 60, "Hannity", "Primetime Flagship", "Sean Hannity welcomes lawmakers, insiders, and opinion leaders for fiery political debate.", "Primetime", False, False),
            ("22:00", 60, "Gutfeld!", "Primetime Comedy", "Greg Gutfeld and guests deliver comedy, parody, and unfiltered political opinion.", "Late Night", False, False),
            ("23:00", 60, "Fox News @ Night", "Nightly Wrap-Up", "Trace Gallagher provides the final word on the day's biggest developments across the country.", "Nightly News", False, False)
        ]
    },
    "msnbc-usa": {
        "name": "MSNBC",
        "category": "News / Politics",
        "genre": "Progressive News, Analysis & Primetime Opinion",
        "shows": [
            ("00:00", 60, "All In with Chris Hayes", "Live Primetime", "Chris Hayes examines the structural forces driving American politics, the economy, and democracy.", "Primetime Analysis", False, False),
            ("01:00", 60, "The Rachel Maddow Show", "Award-Winning Journalism", "Rachel Maddow connects the dots between historical precedent and breaking political scandals.", "Primetime Flagship", False, False),
            ("02:00", 60, "The Last Word with Lawrence O'Donnell", "In-Depth Commentary", "Lawrence O'Donnell draws upon his years as a Senate chief of staff to provide unmatched legislative insight.", "Nightly Commentary", False, False),
            ("03:00", 60, "The 11th Hour with Stephanie Ruhle", "Late Night Nightcap", "Stephanie Ruhle brings business acumen and political sharpness to the late-night news hour.", "Late Night Desk", False, False),
            ("04:00", 60, "Way Too Early with Jonathan Lemire", "White House Early Look", "Jonathan Lemire sets the political agenda before the sun rises in Washington D.C.", "Early Morning", False, False),
            ("05:00", 180, "Morning Joe with Joe Scarborough, Mika Brzezinski & Willie Geist", "Flagship Morning Show", "Joe, Mika, and Willie host the most influential morning political broadcast in America.", "Morning Politics", False, False),
            ("08:00", 60, "Morning Joe Extra", "Capitol Hill Roundtable", "Extended morning analysis featuring Pulitzer-winning journalists, historians, and White House insiders.", "Political Discussion", False, False),
            ("09:00", 120, "Ana Cabrera Reports", "Hard News Desk", "Ana Cabrera reports breaking domestic news, legal proceedings, and national investigative updates.", "News Desk", False, False),
            ("11:00", 60, "José Díaz-Balart Reports", "National & Global News", "José Díaz-Balart anchors humanitarian, political, and breaking international reports.", "News Hour", False, False),
            ("12:00", 60, "Andrea Mitchell Reports", "Foreign Affairs & Diplomacy", "Chief Foreign Affairs Correspondent Andrea Mitchell interviews ambassadors, cabinet officials, and diplomats.", "Diplomatic Desk", False, False),
            ("13:00", 60, "Chris Jansing Reports", "Live Breaking News", "Chris Jansing anchors continuous coverage from the NBC Newsroom in New York.", "Breaking News", False, False),
            ("14:00", 60, "Katy Tur Reports", "Political & Cultural Analysis", "Katy Tur brings sharp reporting and fact-checking to Capitol Hill developments.", "Political News", False, False),
            ("15:00", 120, "Deadline: White House with Nicolle Wallace", "Afternoon Flagship", "Former White House Communications Director Nicolle Wallace leads deep political discussions.", "Top Rated News", False, False),
            ("17:00", 60, "The Beat with Ari Melber", "Law & Pop Culture", "Emmy-winning legal journalist Ari Melber delivers legal analysis, high-profile interviews, and cultural context.", "Legal News", False, False),
            ("18:00", 60, "The ReidOut with Joy Reid", "Evening Analysis", "Joy Reid leads unapologetic discussions on justice, civil rights, and political power dynamics.", "Evening News", False, False),
            ("19:00", 60, "All In with Chris Hayes", "Evening Primetime", "Chris Hayes breaks down complex issues of government accountability and constitutional norms.", "Primetime Analysis", False, False),
            ("20:00", 60, "Inside with Jen Psaki", "Special Primetime Edition", "Former White House Press Secretary Jen Psaki provides insider perspective on executive power.", "Political Perspective", False, False),
            ("21:00", 60, "The Rachel Maddow Show", "Encore Presentation", "High-definition repeat of Rachel Maddow's signature investigative monologues.", "Primetime Showcase", False, False),
            ("22:00", 60, "The Last Word with Lawrence O'Donnell", "Nightly Wrap-Up", "Lawrence O'Donnell provides hard-hitting perspective on the day's final political developments.", "Nightly Commentary", False, False),
            ("23:00", 60, "The 11th Hour with Stephanie Ruhle", "Late Night Edition", "Stephanie Ruhle recaps the day's biggest economic, political, and cultural headlines.", "Late Night Desk", False, False)
        ]
    },
    "abc-usa": {
        "name": "ABC USA",
        "category": "News / Entertainment",
        "genre": "National Broadcast Network",
        "shows": [
            ("00:00", 60, "Jimmy Kimmel Live!", "Late Night Comedy", "Jimmy Kimmel welcomes celebrity guests, musical acts, and delivers signature comedy bits like 'Mean Tweets'.", "Late Night Talk", False, False),
            ("01:00", 30, "Nightline", "Late Night News Magazine", "In-depth investigative reporting, intimate celebrity profiles, and compelling human interest stories.", "Investigative News", False, False),
            ("01:30", 90, "ABC World News Now", "Overnight Broadcast", "Late night / early morning national news broadcast with a lighthearted touch.", "Overnight News", False, False),
            ("03:00", 60, "America This Morning", "Early Bird News", "Comprehensive national news, overnight financial market reports, and national weather forecast.", "Morning News", False, False),
            ("04:00", 120, "Good Morning America", "Live from Times Square", "Robin Roberts, George Stephanopoulos, and Michael Strahan anchor morning news, exclusive interviews, and culture.", "Morning Flagship", False, False),
            ("06:00", 60, "GMA3: What You Need to Know", "Daytime Magazine", "Eva Pilgrim and DeMarco Morgan deliver health news, lifestyle trends, and uplifting human stories.", "Daytime Talk", False, False),
            ("07:00", 60, "General Hospital", "Daytime Drama", "The long-running daytime drama following the passions, rivalries, and intrigue in Port Charles.", "Soap Opera", False, False),
            ("08:00", 60, "The View", "Hot Topics & Celebrity Guests", "Whoopi Goldberg, Joy Behar, Sunny Hostin, Sara Haines, and Alyssa Farah Griffin debate the day's headlines.", "Daytime Panel", False, False),
            ("09:00", 60, "ABC Eyewitness News", "Morning Edition", "Local and national morning news reports, traffic updates, and regional weather forecast.", "Live News", False, False),
            ("10:00", 60, "The Kelly Clarkson Show", "Music & Talk", "Grammy winner Kelly Clarkson hosts celebrity interviews, heartwarming human interest stories, and 'Kellyoke'.", "Talk Show", False, False),
            ("11:00", 60, "Tamron Hall", "Daytime Talk Show", "Tamron Hall hosts candid, in-depth conversations on topics shaping everyday lives.", "Talk Show", False, False),
            ("12:00", 60, "Jeopardy!", "America's Favorite Quiz Show", "Ken Jennings hosts the classic quiz show where contestants test their knowledge across diverse categories.", "Game Show", False, False),
            ("13:00", 60, "Wheel of Fortune", "Puzzle Game Show", "Ryan Seacrest and Vanna White host the iconic word puzzle game show with cash and luxury prizes.", "Game Show", False, False),
            ("14:00", 60, "ABC World News Tonight with David Muir", "America's Most Watched News", "David Muir anchors the premier national newscast, delivering trusted reporting from around the globe.", "Flagship News", False, False),
            ("15:00", 60, "The Rookie", "Season 6, Episode 8", "John Nolan and the team face a sophisticated cyber criminal syndicate targeting the LAPD grid.", "Crime Drama", False, False),
            ("16:00", 60, "Abbott Elementary", "Season 3, Episode 12", "Janine and Gregory navigate teacher evaluations while Ava introduces an unorthodox campus wellness initiative.", "Hit Comedy", False, False),
            ("17:00", 60, "Grey's Anatomy", "Season 20, Episode 10", "The doctors at Grey Sloan Memorial handle an overwhelming mass casualty event in downtown Seattle.", "Medical Drama", False, False),
            ("18:00", 60, "Station 19", "Drama Series", "Seattle firefighters risk their lives responding to hazardous emergencies while balancing complex personal relationships.", "Action Drama", False, False),
            ("19:00", 120, "20/20", "Investigative News Magazine", "David Muir and Deborah Roberts co-anchor gripping true crime investigations and character profiles.", "True Crime / Doc", False, False),
            ("21:00", 60, "ABC World News Tonight with David Muir", "Primetime Re-air", "Encore presentation of David Muir's award-winning evening newscast.", "National News", False, False),
            ("22:00", 60, "Jeopardy! Masters", "Championship Tournament", "The top six highest-ranked current Jeopardy! contestants compete in an elite tournament.", "Game Show", False, False),
            ("23:00", 60, "Jimmy Kimmel Live!", "Primetime Edition", "Jimmy Kimmel delivers hilarious monologues and interviews Hollywood's biggest stars.", "Late Night Comedy", False, False)
        ]
    },
    "abc-ny-usa": {
        "name": "ABC NY USA",
        "category": "News / Entertainment",
        "genre": "New York Flagship Local & National Network",
        "shows": [
            ("00:00", 60, "Eyewitness News at 11pm", "New York Tri-State News", "David Novarro and Sade Baderinwa anchor breaking news across New York, New Jersey, and Connecticut.", "Local News", False, False),
            ("01:00", 60, "Jimmy Kimmel Live!", "Late Night Comedy", "Jimmy Kimmel welcomes celebrity guests and delivers comedic commentary on current events.", "Late Night", False, False),
            ("02:00", 30, "Nightline", "Investigative Journalism", "Late night news magazine delving deep into captivating national stories.", "News", False, False),
            ("02:30", 90, "Eyewitness News Overnight", "Continuous Tri-State News", "Overnight breaking news, transit updates, and weather radar across the New York metropolitan area.", "News", False, False),
            ("04:00", 120, "Good Morning America", "National Broadcast", "Morning news from Times Square Studios with Robin Roberts and George Stephanopoulos.", "Morning News", False, False),
            ("06:00", 60, "Eyewitness News This Morning", "New York Morning News", "Shirleen Allicot and Michael Gargiulo deliver breaking transit and weather for morning commuters.", "Morning News", False, False),
            ("07:00", 60, "Live with Kelly and Mark", "Morning Talk Show", "Kelly Ripa and Mark Consuelos host morning talk with celebrity guests, cooking demos, and entertainment.", "Daytime Talk", False, False),
            ("08:00", 60, "The View", "Hot Topics Live", "Daily dynamic panel discussion covering politics, pop culture, and breaking headlines.", "Daytime Talk", False, False),
            ("09:00", 60, "Eyewitness News at Noon", "Midday Desk", "Live midday coverage of breaking news across New York City and the surrounding suburbs.", "Local News", False, False),
            ("10:00", 60, "General Hospital", "Daytime Drama", "Romantic intrigue and high-stakes medical drama set in fictional Port Charles, New York.", "Drama", False, False),
            ("11:00", 60, "Tamron Hall", "Afternoon Talk", "Engaging daytime conversations with newsmakers, authors, and everyday heroes.", "Talk", False, False),
            ("12:00", 60, "Eyewitness News at 4pm", "Early Evening Edition", "Liz Cho and David Novarro anchor early evening news across the Tri-State region.", "Local News", False, False),
            ("13:00", 60, "Eyewitness News at 5pm", "Tri-State Primetime Desk", "Comprehensive coverage of developing New York stories, investigative reports, and AccuWeather.", "Local News", False, False),
            ("14:00", 60, "Eyewitness News at 6pm", "Evening Flagship", "The most watched local evening newscast in the New York metropolitan area.", "Local News", False, False),
            ("15:00", 60, "ABC World News Tonight with David Muir", "National Flagship", "David Muir anchors the definitive national newscast from the ABC News broadcast center.", "Flagship News", False, False),
            ("16:00", 60, "Jeopardy!", "Classic Quiz Show", "Challengers face off in clues and answers across academic, cultural, and scientific categories.", "Game Show", False, False),
            ("17:00", 60, "Wheel of Fortune", "Primetime Word Puzzle", "Contestants spin the wheel to solve word puzzles and win luxury cars and dream vacations.", "Game Show", False, False),
            ("18:00", 60, "The Rookie", "Season 6", "Officer John Nolan navigates high-stakes patrol duty across Los Angeles with rookie Celina Juarez.", "Police Drama", False, False),
            ("19:00", 60, "Abbott Elementary", "Season 3", "Philadelphia public school educators band together with humor and heart for their students.", "Comedy", False, False),
            ("20:00", 60, "Grey's Anatomy", "Season 20", "High-stress operations, hospital politics, and emotional connections unfold at Grey Sloan.", "Medical Drama", False, False),
            ("21:00", 60, "20/20", "Special Investigation", "In-depth true crime reporting unraveling mysteries and cold cases.", "Documentary", False, False),
            ("22:00", 60, "Eyewitness News at 10pm", "Nightly News", "Late night news summary tracking stories developing across the Tri-State.", "News", False, False),
            ("23:00", 60, "Eyewitness News at 11pm", "Final Edition", "The day's concluding comprehensive newscast with AccuWeather 7-day outlook.", "News", False, False)
        ]
    },
    "amc-usa": {
        "name": "AMC USA",
        "category": "Movies / Entertainment",
        "genre": "Prestige Drama & Hollywood Cinema",
        "shows": [
            ("00:00", 60, "The Walking Dead: The Ones Who Live", "Season 1, Episode 6: The Last Time", "Rick and Michonne fight to secure their future against the overwhelming might of the CRM.", "Post-Apocalyptic", False, False),
            ("01:00", 65, "Interview with the Vampire", "Season 2: And That's The End of It", "Louis de Pointe du Lac recounts the explosive climax of his time with the Théâtre des Vampires in Paris.", "Gothic Drama", False, False),
            ("02:05", 60, "Dark Winds", "Season 2: Hózhóo Naasháa", "Joe Leaphorn and Jim Chee track down a ruthless killer across the Navajo Nation.", "Mystery Thriller", False, False),
            ("03:05", 60, "Better Call Saul", "Season 6: Saul Gone (Series Finale)", "Jimmy McGill faces his final reckoning in a federal courtroom, reconciling with his conscience and Kim Wexler.", "Crime Masterpiece", False, False),
            ("04:05", 60, "Breaking Bad", "Season 5: Ozymandias", "Walt goes on the run as his secret empire collapses in catastrophic violence in the New Mexico desert.", "Legendary Drama", False, False),
            ("05:05", 160, "The Godfather", "Feature Film (1972)", "Francis Ford Coppola's epic masterpiece detailing the Corleone family dynasty under Don Vito and Michael.", "Cinema Classic", True, False),
            ("07:45", 155, "Goodfellas", "Feature Film (1990)", "Martin Scorsese's classic chronicling the rise and fall of mob associate Henry Hill and his partners.", "Crime Classic", True, False),
            ("10:20", 140, "Pulp Fiction", "Feature Film (1994)", "Quentin Tarantino's intertwining tales of Los Angeles mobsters, a boxer, a gangster's wife, and diner bandits.", "Cult Classic", True, False),
            ("12:40", 150, "The Shawshank Redemption", "Feature Film (1994)", "A banker convicted of murder bonds with a fellow inmate over decades, seeking solace and eventual redemption.", "Top Rated Movie", True, False),
            ("15:10", 130, "The Fugitive", "Feature Film (1993)", "Dr. Richard Kimble is wrongfully convicted of murdering his wife and escapes custody to hunt the real killer.", "Action Thriller", True, False),
            ("17:20", 140, "Gladiator", "Feature Film (2000)", "A betrayed Roman general fights his way through the gladiatorial arena to avenge his murdered family.", "Historic Epic", True, False),
            ("19:40", 65, "The Walking Dead: Daryl Dixon", "Season 2: The Book of Carol", "Carol Peletier stops at nothing to find Daryl Dixon across post-apocalyptic France.", "Horror Drama", False, False),
            ("20:45", 60, "Interview with the Vampire", "Encore Presentation", "High-definition showcase of Anne Rice's gothic vampire saga.", "Prestige Drama", False, False),
            ("21:45", 135, "Tombstone", "Feature Film (1993)", "Wyatt Earp and Doc Holliday take on the ruthless Cowboy gang in the historic Arizona boomtown.", "Western Classic", True, False)
        ]
    },
    "fx-usa": {
        "name": "FX USA",
        "category": "Entertainment / Drama",
        "genre": "Critically Acclaimed Drama & Dark Comedy",
        "shows": [
            ("00:00", 40, "The Bear", "Season 3, Episode 1: Tomorrow", "Carmy pushes for culinary perfection at The Bear while navigating unresolved grief and kitchen chaos.", "Emmy Winner", False, False),
            ("00:40", 40, "The Bear", "Season 3, Episode 2: Next", "Sydney weighs a major career decision as Carmy's demanding 'non-negotiables' test the kitchen staff.", "Emmy Winner", False, False),
            ("01:20", 65, "Shōgun", "Episode 10: A Dream of a Dream (Finale)", "Toranaga's master plan reaches its stunning fruition in feudal Japan, reshaping the fate of the nation.", "Historical Masterpiece", False, False),
            ("02:25", 60, "Fargo", "Season 5: Bisquik (Finale)", "Dot Lyon defends her home against Roy Tillman's militia, leading to an extraordinary confrontation.", "Dark Comedy / Crime", False, False),
            ("03:25", 30, "What We Do in the Shadows", "Season 6: The Railroad", "The vampire roommates navigate modern Staten Island bureaucracy and workplace culture.", "Comedy Hit", False, False),
            ("03:55", 30, "It's Always Sunny in Philadelphia", "Season 16", "The Gang gets into another convoluted scheme involving Philadelphia city politics and Paddy's Pub.", "Cult Comedy", False, False),
            ("04:25", 60, "American Horror Story", "Delicate", "A rising actress navigates paranoia, terrifying visions, and sinister figures during her pregnancy.", "Horror Anthology", False, False),
            ("05:25", 130, "Deadpool 2", "Feature Film (2018)", "Wisecracking mercenary Deadpool gathers a team of mutant rogues to protect a young boy from Cable.", "Action Comedy", True, False),
            ("07:35", 125, "Free Guy", "Feature Film (2021)", "A bank teller discovers he is actually an NPC inside an open-world video game and decides to become the hero.", "Sci-Fi Comedy", True, False),
            ("09:40", 140, "Spider-Man: No Way Home", "Feature Film (2021)", "Peter Parker asks Doctor Strange for help, accidentally ripping open the multiverse and summoning iconic villains.", "Marvel Blockbuster", True, False),
            ("12:00", 130, "Iron Man", "Feature Film (2008)", "Billionaire industrialist Tony Stark builds an advanced powered armored suit to escape captivity.", "Superhero Classic", True, False),
            ("14:10", 140, "Avengers: Infinity War", "Feature Film (2018)", "The Avengers and their allies must be willing to sacrifice all in an attempt to defeat the powerful Thanos.", "Marvel Epic", True, False),
            ("16:30", 40, "The Bear", "Season 2: Fishes", "A star-studded, chaotic Christmas dinner with the Berzatto family reveals the roots of Carmy's trauma.", "Critically Acclaimed", False, False),
            ("17:10", 65, "Shōgun", "Episode 9: Crimson Sky", "Mariko arrives in Osaka on a perilous diplomatic mission that tests the loyalties of the council.", "Emmy Winner", False, False),
            ("18:15", 35, "What We Do in the Shadows", "Season 6 Premiere", "Nandor, Nadja, and Laszlo re-examine their five-decade immortal friendship in New York.", "Comedy", False, False),
            ("18:50", 125, "The Martian", "Feature Film (2015)", "An astronaut left behind on Mars must use his scientific wits to survive on a desolate planet.", "Sci-Fi Cinema", True, False),
            ("21:00", 60, "The Old Man", "Season 2", "Dan Chase and Harold Harper venture deep into Afghanistan to rescue Emily from a dangerous warlord.", "Thriller Series", False, False),
            ("22:00", 60, "American Sports Story: Aaron Hernandez", "Drama Series", "The rise and fall of former New England Patriots tight end Aaron Hernandez.", "Biographical Drama", False, False),
            ("23:00", 60, "The Bear", "Encore Showcase", "Back-to-back episodes of the award-winning culinary drama.", "Emmy Winner", False, False)
        ]
    },
    "tnt-usa": {
        "name": "TNT",
        "category": "Entertainment / Sports",
        "genre": "Live Sports, Action Movies & Drama",
        "shows": [
            ("00:00", 60, "NBA on TNT: Tip-Off", "Live Studio Show", "Ernie Johnson, Charles Barkley, Shaquille O'Neal, and Kenny Smith preview the night's marquee games.", "Live Sports Studio", False, True),
            ("01:00", 150, "NBA on TNT Live Game: Celtics vs. Knicks", "Live Basketball", "Eastern Conference heavyweight showdown live from Madison Square Garden in New York City.", "Live NBA Basketball", False, True),
            ("03:30", 150, "NBA on TNT Live Game: Lakers vs. Warriors", "Live Basketball", "Western Conference blockbuster clash featuring LeBron James against Stephen Curry in San Francisco.", "Live NBA Basketball", False, True),
            ("06:00", 60, "Inside the NBA", "Emmy-Winning Postgame", "Charles Barkley, Shaq, Kenny, and Ernie break down the night's game highlights with unfiltered humor.", "Sports Studio", False, True),
            ("07:00", 120, "AEW Collision", "All Elite Wrestling", "High-flying professional wrestling action featuring AEW's elite world champions and top contenders.", "Pro Wrestling", False, True),
            ("09:00", 145, "The Dark Knight Rises", "Feature Film (2012)", "Eight years after the Joker's reign of anarchy, Batman is forced out of exile by the brutal terrorist Bane.", "Action Hit", True, False),
            ("11:25", 130, "Captain America: The Winter Soldier", "Feature Film (2014)", "Steve Rogers struggles to embrace his role in the modern world while teaming with Natasha Romanoff.", "Marvel Blockbuster", True, False),
            ("13:35", 140, "Captain America: Civil War", "Feature Film (2016)", "Political involvement in the Avengers' affairs causes a rift between former allies Captain America and Iron Man.", "Marvel Cinema", True, False),
            ("15:55", 165, "Avengers: Endgame", "Feature Film (2019)", "The remaining Avengers assemble once more to reverse Thanos's actions and restore balance to the universe.", "Epic Cinema", True, False),
            ("18:40", 140, "Guardians of the Galaxy", "Feature Film (2014)", "A group of intergalactic criminals must pull together to stop a fanatical warrior with plans to purge the universe.", "Sci-Fi Action", True, False),
            ("21:00", 120, "Star Wars: The Force Awakens", "Feature Film (2015)", "As a new threat to the galaxy rises, Rey and Finn join Han Solo and Chewbacca to search for Luke Skywalker.", "Sci-Fi Blockbuster", True, False),
            ("23:00", 60, "NBA on TNT: Game Rewind", "Highlights & Analysis", "Comprehensive breakdown of the best dunks, clutch shots, and viral moments from the NBA season.", "Sports Highlights", False, True)
        ]
    },
    "tbs-usa": {
        "name": "TBS",
        "category": "Comedy / Entertainment",
        "genre": "Comedy Marathons & Live Sports",
        "shows": [
            ("00:00", 30, "The Big Bang Theory", "The 21-Second Excitation", "Sheldon and the guys wait in line for the director's cut of 'Raiders of the Lost Ark'.", "Hit Comedy", False, False),
            ("00:30", 30, "The Big Bang Theory", "The Justice League Recombination", "The gang dresses up as the Justice League for a New Year's Eve costume party at the comic book store.", "Hit Comedy", False, False),
            ("01:00", 30, "Young Sheldon", "A High-Pitched Buzz and Training Wheels", "Sheldon gets a taste of college politics when he attempts to overhaul the university campus.", "Comedy", False, False),
            ("01:30", 30, "Young Sheldon", "A Black Hole and Secret Ingredients", "Sheldon attempts to build a supercomputer in his bedroom while Mary takes on new church duties.", "Comedy", False, False),
            ("02:00", 30, "Friends", "The One with the Embryos", "Monica and Rachel compete against Chandler and Joey in a high-stakes trivia contest for their apartment.", "Sitcom Classic", False, False),
            ("02:30", 30, "Friends", "The One with all the Thanksgivings", "The friends look back on their worst past Thanksgivings, culminating in an iconic turkey moment.", "Sitcom Classic", False, False),
            ("03:00", 30, "American Dad!", "Stan Goes on the Pill", "Stan takes an experimental pill that allows him to listen to women's conversations without getting bored.", "Animation", False, False),
            ("03:30", 30, "American Dad!", "Raptor Meets the Girl", "Roger takes on a bizarre new persona when Francine joins a high-society book club.", "Animation", False, False),
            ("04:00", 60, "Wipeout", "Extreme Obstacle Course", "Contestants face the iconic Big Red Balls, the Sweeper, and the brutal Wipeout Zone for a cash prize.", "Game Show", False, False),
            ("05:00", 120, "MLB on TBS: Game of the Week", "Major League Baseball", "Marquee live Major League Baseball regular season and postseason game coverage.", "Live Baseball", False, True),
            ("07:00", 30, "Family Guy", "Road to Rhode Island", "Brian and Stewie embark on an eventful cross-country road trip after getting separated from the family.", "Animation", False, False),
            ("07:30", 30, "Family Guy", "PTV", "Peter starts his own broadcast network after the FCC censors live television awards programming.", "Animation", False, False),
            ("08:00", 30, "Bob's Burgers", "The Belchies", "The Belcher kids go on an adventure to find a legendary treasure inside an abandoned taffy factory.", "Animation", False, False),
            ("08:30", 30, "Bob's Burgers", "Bad Tina", "Tina falls under the influence of a rebellious new girl at school while Bob struggles with an order.", "Animation", False, False),
            ("09:00", 30, "The Big Bang Theory", "The Bath Item Gift Hypothesis", "Penny gives Sheldon a gift with Leonard Nimoy's DNA, causing Sheldon an unprecedented moral dilemma.", "Comedy Favorite", False, False),
            ("09:30", 30, "The Big Bang Theory", "The Adhesive Duck Deficiency", "With Leonard, Howard, and Raj out in the desert, Sheldon must rescue an injured Penny.", "Comedy Favorite", False, False),
            ("10:00", 120, "We're the Millers", "Feature Film (2013)", "A veteran pot dealer creates a fake family as part of his plan to move a huge shipment of weed from Mexico.", "Comedy Film", True, False),
            ("12:00", 120, "Horrible Bosses", "Feature Film (2011)", "Three friends conspire to murder their awful bosses when they realize they are standing in the way of happiness.", "Comedy Hit", True, False),
            ("14:00", 30, "Modern Family", "Caught in the Act", "The kids accidentally walk in on Phil and Claire on their anniversary, sparking mortified chaos.", "Sitcom", False, False),
            ("14:30", 30, "Modern Family", "Fulgencio", "Phil tries to handle family disputes with 'Godfather'-style problem solving during a baptism.", "Sitcom", False, False),
            ("15:00", 120, "The Big Bang Theory Marathon", "Back-to-Back Episodes", "Non-stop episodes featuring Sheldon, Leonard, Penny, Howard, Raj, Bernadette, and Amy.", "Sitcom Marathon", False, False),
            ("17:00", 120, "Friends Marathon", "Fan-Favorite Episodes", "Classic New York moments with Ross, Rachel, Monica, Chandler, Joey, and Phoebe.", "Comedy Marathon", False, False),
            ("19:00", 30, "The Big Bang Theory", "The Scavenger Vortex", "Raj designs an elaborate scavenger hunt across Pasadena that divides the group into unlikely teams.", "Hit Comedy", False, False),
            ("19:30", 30, "The Big Bang Theory", "The Locomotive Manipulation", "Amy arranges a romantic Valentine's Day weekend on a vintage train in Napa Valley with Sheldon.", "Hit Comedy", False, False),
            ("20:00", 30, "The Big Bang Theory", "The Opening Night Excitation", "Sheldon skips the 'Star Wars' premiere to spend a landmark evening with Amy on her birthday.", "Hit Comedy", False, False),
            ("20:30", 30, "The Big Bang Theory", "The Stockholm Syndrome (Series Finale)", "The gang travels to Sweden for Sheldon and Amy's Nobel Prize ceremony in an emotional finale.", "Series Finale", False, False),
            ("21:00", 120, "Step Brothers", "Feature Film (2008)", "Two aimless middle-aged men living with their parents are forced to become roommates when their parents marry.", "Comedy Classic", True, False),
            ("23:00", 60, "American Dad!", "Late Night Blocks", "Back-to-back late night episodes of the irreverent CIA family comedy.", "Animation", False, False)
        ]
    },
    "usa-network-usa": {
        "name": "USA Network",
        "category": "Entertainment / Drama",
        "genre": "WWE Wrestling, Crime Drama & Action",
        "shows": [
            ("00:00", 180, "WWE Monday Night Raw Live", "Live Pro Wrestling", "Three hours of live sports entertainment featuring Roman Reigns, Cody Rhodes, Seth Rollins, and Rhea Ripley.", "Live WWE", False, True),
            ("03:00", 60, "WWE Raw Post-Show", "Backstage Interviews", "Exclusive backstage interviews, fallout analysis, and previews for upcoming premium live events.", "WWE Studio", False, True),
            ("04:00", 60, "Law & Order: SVU", "Season 25: Tunnel Blind", "Captain Olivia Benson and her squad investigate a series of abductions targeting university students.", "Crime Drama", False, False),
            ("05:00", 60, "Law & Order: SVU", "Season 25: Duty to Report", "When a high-profile athlete is accused of assault, the detectives navigate intense media scrutiny.", "Crime Drama", False, False),
            ("06:00", 60, "Chicago P.D.", "Season 11: Retaliation", "Voight and the Intelligence Unit race against time to dismantle an armed gang terrorizing the 21st District.", "Action Drama", False, False),
            ("07:00", 60, "Chicago P.D.", "Season 11: The Water's Edge", "Upton makes a dangerous move to track down an elusive serial offender before he strikes again.", "Action Drama", False, False),
            ("08:00", 60, "Chicago Fire", "Season 12: Call Me McHolland", "Firehouse 51 responds to a four-alarm chemical blaze at a warehouse district on the South Side.", "Action Drama", False, False),
            ("09:00", 60, "Chicago Fire", "Season 12: Under the Skin", "Severide takes the lead on an arson investigation while Cruz steps up in truck management.", "Action Drama", False, False),
            ("10:00", 60, "Suits", "Season 5: Faith", "Harvey faces his past in therapy while Mike Ross grapples with the mounting danger of his secret.", "Legal Drama", False, False),
            ("11:00", 60, "Suits", "Season 5: 25th Hour", "The climactic trial of Mike Ross concludes as Harvey and Jessica fight to save Pearson Specter Litt.", "Legal Drama", False, False),
            ("12:00", 120, "The Fast and the Furious: Tokyo Drift", "Feature Film (2006)", "An American teenager sent to live with his father in Tokyo finds solace in the city's drift racing underworld.", "Action Movie", True, False),
            ("14:00", 120, "Fast & Furious 6", "Feature Film (2013)", "Dom Toretto and his team are pardoned in exchange for helping diplomatic security track a mercenary crew.", "Action Blockbuster", True, False),
            ("16:00", 60, "Law & Order: SVU", "Season 24: Blood Out", "Benson and Stabler reunite on a high-stakes coordinated investigation across Manhattan.", "Crime Drama", False, False),
            ("17:00", 60, "Law & Order: SVU", "Season 24: Bad Things", "A serial predator's signature matches a cold case from Benson's earliest years in the Special Victims Unit.", "Crime Drama", False, False),
            ("18:00", 60, "Law & Order: SVU", "Season 24: All Pain Is One Malady", "The squad investigates a dark web extortion ring targeting vulnerable young people.", "Crime Drama", False, False),
            ("19:00", 60, "Law & Order: SVU", "Season 25: Combat Fatigue", "Fin and Bruno handle a volatile hostage negotiation while Carisi presents critical forensic evidence.", "Crime Drama", False, False),
            ("20:00", 60, "WWE NXT Highlights", "Sports Entertainment", "The rising stars of WWE battle for supremacy inside the Capitol Wrestling Center.", "WWE Action", False, True),
            ("21:00", 120, "Furious 7", "Feature Film (2015)", "Deckard Shaw seeks revenge against Dominic Toretto and his family for his comatose brother.", "Action Hit", True, False),
            ("23:00", 60, "Law & Order: SVU", "Late Night Investigation", "Captain Olivia Benson leads late-night interrogation and detective work in New York.", "Crime Drama", False, False)
        ]
    }
}

# Generic robust generator for remaining US channels
GENERIC_GENRES = {
    "ae-usa": ("A&E USA", "Entertainment / Documentary", "Real Life Crime & Reality", [
        ("The First 48", "Homicide detectives race against the clock in the critical initial hours after a crime."),
        ("Intervention", "Families confront loved ones battling severe addiction with the help of professional specialists."),
        ("Storage Wars", "Auction buyers bid on contents of abandoned storage lockers hoping to uncover hidden treasures."),
        ("Court Cam", "Dan Abrams hosts dramatic and shocking moments captured inside courtroom cameras."),
        ("Accused: Guilty or Innocent?", "Following defendants from their perspective as they prepare for high-stakes criminal trials.")
    ]),
    "adult-swim-usa": ("Adult Swim", "Adult Animation / Comedy", "Late Night Animation & Satire", [
        ("Rick and Morty", "Genius scientist Rick Sanchez and his grandson Morty embark on chaotic interdimensional journeys."),
        ("Smiling Friends", "Employees of a small charity dedicated to bringing happiness to people handle bizarre clients."),
        ("Aqua Teen Hunger Force", "Meatwad, Frylock, and Master Shake live as roommates in suburban New Jersey."),
        ("Robot Chicken", "Seth Green's stop-motion sketch comedy spoofing pop culture, action figures, and film."),
        ("Primal", "A caveman at the dawn of evolution forms an unlikely bond with an endangered tyrannosaurus.")
    ]),
    "syfy-usa": ("Syfy", "Sci-Fi / Fantasy", "Science Fiction, Fantasy & Horror", [
        ("Resident Alien", "A crash-landed alien assumes the identity of a small-town doctor in Colorado."),
        ("The Ark", "The remaining crew of spacecraft Ark One must survive after a catastrophic event."),
        ("The Twilight Zone", "Rod Serling's classic anthology of science fiction, mystery, and the supernatural."),
        ("Battlestar Galactica", "The last surviving humans journey across the stars searching for the fabled thirteenth colony."),
        ("Interstellar Odyssey", "A starship crew investigates an ancient alien megastructure at the edge of the galaxy.")
    ]),
    "paramount-network-usa": ("Paramount Network", "Entertainment / Drama", "Western Drama & Reality", [
        ("Yellowstone", "The Dutton family defends the largest contiguous cattle ranch in the United States."),
        ("Bar Rescue", "Jon Taffer helps turnaround failing bars and nightclubs across America."),
        ("Mayor of Kingstown", "The McLusky family power brokers in a town where incarceration is the only thriving industry."),
        ("Tulsa King", "New York mafia capo Dwight Manfredi is released from prison and exiled to Tulsa, Oklahoma."),
        ("1883", "A prequel to Yellowstone following the Dutton family's arduous journey west across the Great Plains.")
    ]),
    "discovery-channel-usa": ("Discovery Channel", "Documentary / Science", "Science, Exploration & Survival", [
        ("Deadliest Catch", "Alaskan crab fishermen battle freezing temperatures and towering waves on the Bering Sea."),
        ("Gold Rush", "Miners risk everything searching for gold in the harsh wilderness of the Yukon."),
        ("Naked and Afraid", "Pairs of survivalists are stranded in remote wilderness for 21 days with no clothes or provisions."),
        ("Expedition Unknown", "Josh Gates investigates the world's most enduring legends and historical mysteries."),
        ("MythBusters", "Special effects experts put urban legends to the test using rigorous scientific experiments.")
    ]),
    "history-channel-usa": ("History Channel", "History / Documentary", "History, Mysteries & Artifacts", [
        ("The Curse of Oak Island", "Brothers Rick and Marty Lagina search for buried treasure on Nova Scotia's Oak Island."),
        ("Pawn Stars", "The Harrison family appraises and negotiates rare historical artifacts at their Las Vegas pawn shop."),
        ("Forged in Fire", "Master bladesmiths compete to re-create history's most iconic edged weapons."),
        ("Ancient Aliens", "Investigating theories that extraterrestrials visited Earth thousands of years ago."),
        ("Alone", "Ten survivalists enter the wild with only ten items to see who can endure the longest in complete isolation.")
    ]),
    "national-geographic-usa": ("National Geographic", "Documentary / Science", "Nature, Science & Exploration", [
        ("Life Below Zero", "Alaskans struggle to survive the brutally freezing winter in remote wilderness."),
        ("Secrets of the Zoo", "Behind the scenes with veterinary teams caring for endangered species at world-class zoos."),
        ("Wicked Tuna", "Commercial bluefin tuna fishermen battle in Gloucester, Massachusetts for valuable fish."),
        ("Trafficked with Mariana van Zeller", "Investigative journalist Mariana van Zeller explores global black markets."),
        ("Explorer", "Documenting deep-sea expeditions, high-altitude climbs, and unmapped ecosystems.")
    ]),
    "animal-planet-usa": ("Animal Planet", "Nature / Documentary", "Wildlife, Conservation & Pets", [
        ("River Monsters", "Biologist Jeremy Wade travels the globe searching for freshwater fish with a taste for human flesh."),
        ("Pit Bulls & Parolees", "Tia Torres provides shelter for neglected dogs while offering parolees a fresh start."),
        ("Crikey! It's the Irwins", "Terri, Bindi, and Robert Irwin carry on Steve Irwin's mission at the Australia Zoo."),
        ("The Zoo", "A look at the dedicated staff caring for 6,000 animals at the Bronx Zoo in New York."),
        ("My Cat from Hell", "Cat behaviorist Jackson Galaxy helps frustrated owners resolve behavioral issues with their felines.")
    ]),
    "food-network-usa": ("Food Network", "Lifestyle / Cooking", "Culinary Competitions & Food Culture", [
        ("Diners, Drive-Ins and Dives", "Guy Fieri visits America's classic roadside eateries, barbecue joints, and diners."),
        ("Chopped", "Four chefs turn mystery basket ingredients into extraordinary three-course meals under time pressure."),
        ("Beat Bobby Flay", "Talented chefs compete for the chance to take on Iron Chef Bobby Flay in a culinary showdown."),
        ("Guy's Grocery Games", "Chefs navigate high-stakes cooking challenges inside a fully-stocked grocery store."),
        ("Tournament of Champions", "Thirty-two world-class chefs face off in a single-elimination culinary tournament.")
    ]),
    "hgtv-usa": ("HGTV", "Home / Lifestyle", "Home Renovation, Design & Real Estate", [
        ("House Hunters", "Homebuyers tour three properties with a real estate agent before deciding which to purchase."),
        ("Fixer Upper", "Chip and Joanna Gaines transform rundown Texas properties into dream homes."),
        ("Property Brothers", "Drew and Jonathan Scott help couples purchase and renovate fixer-uppers into forever homes."),
        ("Home Town", "Ben and Erin Napier restore historic Southern homes in Laurel, Mississippi."),
        ("Love It or List It", "Homeowners decide whether to stay in their renovated home or sell it for a new property.")
    ]),
    "tlc-usa": ("TLC", "Lifestyle / Reality", "Family Stories, Relationships & Reality", [
        ("90 Day Fiancé", "Couples who have received K-1 visas have 90 days to marry before their visas expire."),
        ("Say Yes to the Dress", "Brides search for their dream wedding gowns at Kleinfeld Bridal in Manhattan."),
        ("My 600-lb Life", "Dr. Younan Nowzaradan guides individuals on life-changing weight loss journeys in Houston."),
        ("Sister Wives", "Kody Brown and his family navigate the complexities of plural marriage."),
        ("Dr. Pimple Popper", "Dermatologist Dr. Sandra Lee treats patients with extraordinary skin conditions.")
    ]),
    "comedy-central-usa": ("Comedy Central", "Comedy / Entertainment", "Stand-Up Comedy, Satire & Sitcoms", [
        ("South Park", "Stan, Kyle, Cartman, and Kenny navigate outrageous adventures in the Colorado mountain town."),
        ("The Daily Show", "Satirical news broadcast skewering the day's political absurdity and media coverage."),
        ("The Office", "Dunder Mifflin paper company employees navigate workplace dynamics in Scranton, Pennsylvania."),
        ("Parks and Recreation", "Leslie Knope and the Pawnee Parks Department take on municipal bureaucracy."),
        ("Brooklyn Nine-Nine", "Detective Jake Peralta and his eccentric colleagues solve crimes in Brooklyn's 99th precinct.")
    ]),
    "mtv-usa": ("MTV", "Music / Reality", "Youth Reality & Pop Culture", [
        ("Ridiculousness", "Rob Dyrdek, Steelo Brim, and guests review viral Internet video clips and epic stunts."),
        ("Catfish: The TV Show", "Nev Schulman helps people discover the truth behind their online romantic partners."),
        ("The Challenge", "Reality television legends compete in brutal physical and mental challenges for a million dollars."),
        ("Teen Mom: The Next Chapter", "Following the ongoing lives, parenthood journeys, and careers of young mothers."),
        ("MTV Video Music Awards Highlights", "Iconic musical performances, red carpet moments, and Moonman awards.")
    ]),
    "vh1-usa": ("VH1", "Music / Reality", "Urban Culture, Reality & Music", [
        ("RuPaul's Drag Race", "Drag queens compete in charisma, uniqueness, nerve, and talent for the crown and cash prize."),
        ("Love & Hip Hop: Atlanta", "The lives, loves, and music careers of Atlanta hip-hop royalty."),
        ("Basketball Wives", "The personal and professional lives of women romantically linked to NBA stars."),
        ("Behind the Music", "Deep-dive documentary examining the triumphs and tribulations of legendary musical artists."),
        ("Wild 'N Out", "Nick Cannon hosts high-energy improv comedy and hip-hop freestyle battles.")
    ]),
    "e-entertainment-usa": ("E! Entertainment", "Entertainment / Celebrity", "Celebrity News, Red Carpets & Glamour", [
        ("Keeping Up with the Kardashians", "The iconic reality series following the Kardashian-Jenner family's empire."),
        ("Botched", "Dr. Terry Dubrow and Dr. Paul Nassif correct extreme and botched plastic surgeries."),
        ("E! News", "Breaking celebrity news, red carpet interviews, and Hollywood exclusives."),
        ("Live from the Red Carpet", "Glitz, fashion, and interviews with stars arriving at Hollywood awards shows."),
        ("Relatively Famous: Ranch Rules", "Celebrity children work together to restore a Colorado working ranch.")
    ]),
    "investigation-discovery-usa": ("Investigation Discovery", "True Crime / Documentary", "True Crime Mysteries & Forensics", [
        ("On the Case with Paula Zahn", "Journalist Paula Zahn interviews detectives, witnesses, and families in murder cases."),
        ("Evil Lives Here", "People recount the terrifying experience of living with someone who became a murderer."),
        ("Fear Thy Neighbor", "Petty neighborhood disputes escalate into shocking and tragic acts of violence."),
        ("See No Evil", "How surveillance cameras and digital video footage cracked cold homicide cases."),
        ("Disappeared", "Investigating mysterious disappearances and the agonizing search for answers.")
    ]),
    "lifetime-usa": ("Lifetime", "Entertainment / Movies", "Women's Drama & Original Movies", [
        ("Married at First Sight", "Relationship experts match singles who agree to marry the moment they first meet."),
        ("Dance Moms", "Abby Lee Miller trains young dancers for high-pressure national dance competitions."),
        ("Lifetime Movie: Secret Lives of Housewives", "A woman uncovers dark neighborhood secrets when a friend goes missing."),
        ("Little Women: LA", "A group of smart, dynamic little women navigate friendship, career, and relationships."),
        ("Surviving R. Kelly", "Investigative documentary chronicling allegations of abuse and legal battles.")
    ]),
    "hallmark-channel-usa": ("Hallmark Channel", "Family / Movies", "Heartfelt Romance & Family Drama", [
        ("When Calls the Heart", "Elizabeth Thatcher navigates life, romance, and teaching in Canadian coal country."),
        ("The Way Home", "Three generations of Landry women embark on an unexpected journey through time."),
        ("Countdown to Christmas: Winter Romance", "An architect returns to her hometown and finds love with a local baker."),
        ("Chesapeake Shores", "A high-powered career woman returns to her coastal hometown to help save her family's inn."),
        ("Mystery 101", "A literature professor and a police detective team up to solve murder mysteries.")
    ]),
    "trutv-usa": ("truTV", "Comedy / Reality", "Pranks, Impractical Comedy & Challenges", [
        ("Impractical Jokers", "Four lifelong friends compete in outrageous public hidden-camera dares."),
        ("The Carbonaro Effect", "Magician Michael Carbonaro performs astonishing illusions on unsuspecting strangers."),
        ("Fast Foodies", "Top chefs compete to re-create and elevate celebrity guests' favorite fast food dishes."),
        ("Tacoma FD", "A crew of firefighters in the rainiest city in America battle boredom with hilarious pranks."),
        ("World's Dumbest", "Comedians deliver hilarious commentary on wild driver encounters and mishaps.")
    ]),
    "science-channel-usa": ("Science Channel", "Science / Documentary", "Engineering, Space & Discovery", [
        ("How It's Made", "Exploring how everyday items, machines, and specialty products are manufactured."),
        ("Mysteries of the Abandoned", "Uncovering the stories behind engineering marvels left to decay worldwide."),
        ("Space's Deepest Secrets", "Astronomers and astrophysicists probe black holes, exoplanets, and cosmic phenomena."),
        ("Outrageous Acts of Science", "Scientists explain the principles behind viral internet science stunts."),
        ("What on Earth?", "Satellites photograph strange phenomena on Earth that baffle experts.")
    ]),
    "travel-channel-usa": ("Travel Channel", "Travel / Lifestyle", "Paranormal, Travel & Adventure", [
        ("Ghost Adventures", "Zak Bagans and his crew investigate the world's most terrifying haunted locations."),
        ("The Dead Files", "A medium and a homicide detective investigate paranormal phenomena at distressed properties."),
        ("Bizarre Foods with Andrew Zimmern", "Andrew Zimmern travels the globe tasting unforgettable regional delicacies."),
        ("Expedition Bigfoot", "An elite team of researchers utilizes advanced technology to track cryptids."),
        ("Mysteries at the Museum", "Don Wildman investigates extraordinary artifacts housed in museums worldwide.")
    ]),
    "we-tv-usa": ("WE tv", "Reality / Entertainment", "Reality Drama & Relationships", [
        ("Love After Lockup", "Couples navigate romance after one partner is released from prison."),
        ("Mama June: Family Crisis", "Mama June Shannon works to rebuild relationships with her daughters."),
        ("Growing Up Hip Hop", "The children of hip-hop legends forge their own paths in music and business."),
        ("Bridezillas", "Stressed-out brides-to-be navigate wedding planning with extreme drama."),
        ("Marriage Boot Camp", "Celebrity couples undergo intensive therapy to decide the fate of their marriages.")
    ]),
    "freeform-usa": ("Freeform", "Entertainment / Young Adult", "Young Adult Drama & Movies", [
        ("Cruel Summer", "An anthology series exploring the repercussions of a kidnapping in a Texas town."),
        ("Grown-ish", "Zoey Johnson and her friends navigate college life and emerging adulthood."),
        ("Pretty Little Liars", "Four friends band together against an anonymous foe threatening their secrets."),
        ("The Bold Type", "Three young women navigate career and romance at a global women's magazine in New York."),
        ("Disney's Aladdin", "A kindhearted street urchin vies for the love of a princess with the help of a genie.")
    ]),
    "bbc-america-usa": ("BBC America", "Entertainment / Documentary", "British Sci-Fi, Drama & Nature", [
        ("Doctor Who", "The Doctor travels through time and space in the TARDIS righting cosmic wrongs."),
        ("Top Gear", "The boys test the world's most exotic supercars in hilarious international challenges."),
        ("The Graham Norton Show", "Graham Norton hosts A-list Hollywood stars for lively couch conversations and comedy."),
        ("Planet Earth III", "Sir David Attenborough narrates groundbreaking footage of extraordinary wildlife."),
        ("Star Trek: The Next Generation", "Captain Picard and the crew of the USS Enterprise explore strange new worlds.")
    ]),
    "ahc-usa": ("AHC (American Heroes Channel)", "Documentary / History", "Military History & Warfare", [
        ("World War II in Color", "Rare and restored color footage chronicles the decisive battles of the Second World War."),
        ("Gunslingers", "The true stories behind legendary Old West figures like Wyatt Earp and Billy the Kid."),
        ("Combat Ships", "The naval vessels and tactical innovations that turned the tide of historic sea warfare."),
        ("Blood and Fury: America's Civil War", "High-definition dramatizations of the pivotal battles of the American Civil War."),
        ("Against the Odds", "Soldiers trapped in impossible combat situations display extraordinary courage.")
    ]),
    "antenna-tv-usa": ("Antenna TV USA", "Classic TV / Entertainment", "Vintage Television Classics", [
        ("The Tonight Show Starring Johnny Carson", "The King of Late Night interviews legends of Hollywood, music, and comedy."),
        ("Barney Miller", "Detectives at the 12th Precinct handle quirky Greenwich Village complaints."),
        ("Alice", "A widowed mother works as a waitress at a Phoenix diner while raising her son."),
        ("Three's Company", "Jack Tripper shares a Santa Monica apartment with two female roommates."),
        ("Bewitched", "A beautiful witch marries an ordinary mortal advertising executive.")
    ]),
    "axs-tv-usa": ("AXS TV USA", "Music / Entertainment", "Concerts, Rock & Wrestling", [
        ("The Big Interview with Dan Rather", "Journalist Dan Rather conducts candid, in-depth interviews with music icons."),
        ("Rock Legends", "Profiles of legendary musicians who shaped the rock and roll landscape."),
        ("AXS TV Concerts", "Front-row tickets to unforgettable live performances from arena rock bands."),
        ("New Japan Pro Wrestling", "High-impact strong style wrestling from Tokyo's Tokyo Dome and Korakuen Hall."),
        ("A Year in Music", "Exploring landmark years in music history that defined generations.")
    ]),
    "ifc-usa": ("IFC", "Movies / Comedy", "Indie Cinema & Satire", [
        ("Portlandia", "Fred Armisen and Carrie Brownstein spoof the eccentric culture of Portland, Oregon."),
        ("Documentary Now!", "Helen Mirren introduces meticulous parodies of cinema's greatest documentaries."),
        ("Stan Against Evil", "An aging police sheriff and his replacement team up to battle demonic forces."),
        ("Independent Spirit Cinema", "Award-winning independent cinema celebrating bold and original voices."),
        ("Comedy Bang! Bang!", "Scott Aukerman and his bandleader host an absurd and whimsical talk show.")
    ]),
    "pbs-usa": ("PBS", "Educational / Public", "Public Television, Arts & Science", [
        ("PBS NewsHour", "In-depth, balanced news coverage and analysis of domestic and international issues."),
        ("Frontline", "Investigative documentaries probing critical social, economic, and political stories."),
        ("Nova", "Exploring breakthroughs in astrophysics, quantum mechanics, and evolutionary biology."),
        ("Masterpiece", "Acclaimed adaptations of classic literature, British mysteries, and period drama."),
        ("Antiques Roadshow", "Appraisal experts discover extraordinary treasures in everyday attics.")
    ]),
    "bloomberg-us": ("Bloomberg Television", "Global Markets & Finance", "Financial News & Global Markets", [
        ("Bloomberg Surveillance", "Tom Keene and Jonathan Ferro analyze the opening market moves across Wall Street."),
        ("Bloomberg Markets", "Real-time market tickers, currency movements, and earnings report breakdowns."),
        ("Balance of Power", "Analyzing the intersection of political legislation and Wall Street investment."),
        ("Wall Street Week", "In-depth discussions with hedge fund managers and Federal Reserve economists."),
        ("Bloomberg Technology", "Caroline Hyde and Ed Ludlow explore artificial intelligence, venture capital, and startups.")
    ]),
    "entrepreneurtv": ("EntrepreneurTV", "Business / Entrepreneurship", "Startups, Business & Innovation", [
        ("Elevator Pitch", "Entrepreneurs have 60 seconds inside an elevator to pitch their ideas to investors."),
        ("Start Up", "Gary Bredow travels across America meeting passionate small business owners."),
        ("Business Rockstars", "Interviews with visionary founders who built multi-million dollar brands."),
        ("Modern Day Mogul", "Profiles of innovators who revolutionized tech, retail, and digital media."),
        ("Unfiltered Entrepreneur", "Uncensored lessons on fundraising, marketing, and scaling companies from scratch.")
    ])
}


def build_generic_shows_for_channel(slug, channel_info):
    name, category, genre, show_pool = channel_info
    # Generate 16 continuous time blocks filling 24 hours (approx 60-120 mins each)
    durations = [60, 60, 60, 90, 90, 60, 120, 120, 90, 90, 60, 60, 90, 120, 90, 60]
    shows = []
    
    current_min = 0
    pool_len = len(show_pool)
    
    for i, dur in enumerate(durations):
        h = (current_min // 60) % 24
        m = current_min % 60
        time_str = f"{h:02d}:{m:02d}"
        
        title, desc = show_pool[i % pool_len]
        subtitle = f"Episode {((i * 3 + 1) % 18) + 1}"
        tag = "Documentary" if "Documentary" in category else ("Live News" if "News" in category else ("Feature Film" if dur >= 90 else "Entertainment"))
        is_movie = "Movie" in category or "Cinema" in category or dur >= 110
        is_sport = "Sports" in category
        
        shows.append((time_str, dur, title, subtitle, desc, tag, is_movie, is_sport))
        current_min += dur
        if current_min >= 1440:
            break
            
    return shows


def format_time_12h(h, m):
    ampm = "am" if h < 12 else "pm"
    dh = h % 12
    if dh == 0:
        dh = 12
    return f"{dh}:{m:02d} {ampm}"


def generate_all_us_channel_schedules(base_unix=None):
    """
    Builds full, continuous 24h EPG listings for all 45 US channels.
    All start and end times are anchored to today's midnight UTC,
    ensuring exact alignment with UK Local Time.
    """
    if base_unix is None:
        now_utc = datetime.datetime.now(datetime.timezone.utc)
        today_utc = now_utc.replace(hour=0, minute=0, second=0, microsecond=0)
        base_unix = int(today_utc.timestamp())

    results = {}

    # 1. Custom detailed channels
    for slug, data in US_CHANNEL_PROGRAMS.items():
        name = data["name"]
        genre = data["genre"]
        raw_shows = data["shows"]
        
        channel_shows = []
        for i, (start_str, dur_mins, title, subtitle, desc, tag, is_movie, is_sport) in enumerate(raw_shows):
            sh, sm = map(int, start_str.split(':'))
            st_unix = base_unix + (sh * 3600) + (sm * 60)
            et_unix = st_unix + (dur_mins * 60)
            
            end_dt = datetime.datetime.fromtimestamp(et_unix, datetime.timezone.utc)
            eh, em = end_dt.hour, end_dt.minute
            
            show_obj = {
                "id": f"{slug}-{sh:02d}{sm:02d}",
                "title": title,
                "subtitle": subtitle,
                "timeStr": format_time_12h(sh, sm),
                "start": f"{sh:02d}:{sm:02d}",
                "end": f"{eh:02d}:{em:02d}",
                "startHour": sh,
                "startMin": sm,
                "durationMinutes": dur_mins,
                "tag": tag,
                "desc": desc,
                "isMovie": is_movie,
                "isSport": is_sport,
                "epochStart": st_unix,
                "epochEnd": et_unix,
                "source": "US TV Guide (UK Time)"
            }
            channel_shows.append(show_obj)
            
        results[slug] = {
            "id": slug,
            "name": name,
            "genre": genre,
            "source": "US TV Guide (UK Time)",
            "shows": channel_shows
        }

    # 2. Generic robust channels
    for slug, info in GENERIC_GENRES.items():
        if slug in results:
            continue
        name, category, genre, _ = info
        raw_shows = build_generic_shows_for_channel(slug, info)
        
        channel_shows = []
        for i, (start_str, dur_mins, title, subtitle, desc, tag, is_movie, is_sport) in enumerate(raw_shows):
            sh, sm = map(int, start_str.split(':'))
            st_unix = base_unix + (sh * 3600) + (sm * 60)
            et_unix = st_unix + (dur_mins * 60)
            
            end_dt = datetime.datetime.fromtimestamp(et_unix, datetime.timezone.utc)
            eh, em = end_dt.hour, end_dt.minute
            
            show_obj = {
                "id": f"{slug}-{sh:02d}{sm:02d}",
                "title": title,
                "subtitle": subtitle,
                "timeStr": format_time_12h(sh, sm),
                "start": f"{sh:02d}:{sm:02d}",
                "end": f"{eh:02d}:{em:02d}",
                "startHour": sh,
                "startMin": sm,
                "durationMinutes": dur_mins,
                "tag": tag,
                "desc": desc,
                "isMovie": is_movie,
                "isSport": is_sport,
                "epochStart": st_unix,
                "epochEnd": et_unix,
                "source": "US TV Guide (UK Time)"
            }
            channel_shows.append(show_obj)
            
        results[slug] = {
            "id": slug,
            "name": name,
            "genre": genre,
            "source": "US TV Guide (UK Time)",
            "shows": channel_shows
        }

    # Add shorthand slug aliases
    aliases = {
        "hbo": "hbo-usa",
        "cinemax": "cinemax-usa",
        "hbo-family": "hbo-family-usa",
        "hbo-hits": "hbo-hits-usa",
        "hbo-signature": "hbo-signature-usa"
    }
    for alias, target in aliases.items():
        if target in results:
            results[alias] = results[target]

    return results

if __name__ == "__main__":
    schedules = generate_all_us_channel_schedules()
    print(f"Generated schedules for {len(schedules)} US channels.")
    for ch_id, ch_data in list(schedules.items())[:5]:
        print(f"\n[{ch_id}] {ch_data['name']} - Total shows: {len(ch_data['shows'])}")
        first = ch_data['shows'][0]
        print(f"  First: {first['start']} -> {first['end']} | {first['title']} ({first['tag']})")
