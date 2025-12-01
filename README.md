# 🎄 CondaCarol - Christmas Party Guessing Game 🐍

A festive web app for your company Christmas party! Learn more about your colleagues through fun questions and guessing games.

## 🎁 What is CondaCarol?

CondaCarol is an interactive party game where:
1. **Admin sets up** interesting questions
2. **Participants answer** questions anonymously
3. **Everyone plays** by guessing who said what
4. **Winners are revealed** with scores and leaderboards!

Perfect for team building, holiday parties, and getting to know your coworkers better!

## 🚀 Quick Start

### Prerequisites
- [Anaconda](https://www.anaconda.com/download) or [Miniconda](https://docs.conda.io/en/latest/miniconda.html) installed

### Setup

1. **Clone this repository**
```bash
git clone <your-repo-url>
cd condacarol
```

2. **Create the conda environment**
```bash
conda env create -f environment.yaml
```

3. **Activate the environment**
```bash
conda activate condacarol
```

4. **Run the app**
```bash
panel serve app.py --show --autoreload
```

The app will open in your browser at `http://localhost:5006`

## 🎮 How to Play

### Phase 1: Setup (Admin)
1. Navigate to the **Setup** tab
2. Enter admin password: `condaclaus2024`
3. Add 3+ questions (fun, personal questions work best!)
4. Click "Start Answer Phase" when ready

Example questions:
- What's your most embarrassing childhood memory?
- If you could have dinner with anyone, who would it be?
- What's the weirdest food combination you enjoy?
- What's your hidden talent?

### Phase 2: Answer Questions (Everyone)
1. Go to the **Answer Questions** tab
2. Enter your name
3. Answer all questions
4. Submit your answers
5. Admin starts the game when everyone has answered

### Phase 3: Play Game (Everyone)
1. Go to the **Play Game** tab
2. Enter your name
3. Read each answer and guess who wrote it
4. Submit your guesses
5. Wait for admin to reveal results

### Phase 4: Results
1. View the leaderboard
2. See all correct answers
3. Crown the winner! 🏆
4. Admin can reset for a new game

## 🔒 Admin Password

Default: `condaclaus2024`

To change it, edit line 21 in `app.py`:
```python
'admin_password': 'your-new-password'
```

## 🌐 Deployment Options

### Option 1: Local Network (Recommended for parties)

Share the app on your local network:

```bash
panel serve app.py --address 0.0.0.0 --port 5006
```

Then share your local IP with participants:
- Find your IP: `ipconfig` (Windows) or `ifconfig` (Mac/Linux)
- Share URL: `http://YOUR-IP:5006`

### Option 2: Panel Cloud (Easiest for remote teams)

Deploy to [Panel Cloud](https://panel.holoviz.org/how_to/deployment/panel_cloud.html):

1. Sign up at panel.holoviz.org
2. Install panel CLI: `pip install panel-cloud`
3. Deploy: `panel cloud deploy app.py`

### Option 3: Heroku / Railway / Render

Panel apps work well on these platforms. Create a `Procfile`:

```
web: panel serve app.py --address 0.0.0.0 --port $PORT
```

### Note on Vercel

Vercel is optimized for serverless/static deployments. Panel apps run as persistent Python servers, making platforms like Heroku, Railway, Render, or Panel Cloud better suited. For Vercel deployment, you'd need to significantly refactor the app to use serverless functions with external state storage (database).

## 🛠️ Customization

### Styling
The app uses Panel's Material design. To customize:
- Change `design='material'` to `design='bootstrap'` or `design='fast'` in line 13
- Modify the template in the last section of `app.py`

### Features to Add
- Persistent storage (save to JSON/database)
- Timer for each phase
- Multiple choice questions
- Photo uploads for answers
- Export results to PDF

## 📝 Development

### Project Structure
```
condacarol/
├── app.py              # Main Panel application
├── environment.yaml    # Conda dependencies
├── README.md          # This file
└── .gitignore         # Git ignore rules
```

### Running in Development Mode
```bash
conda activate condacarol
panel serve app.py --show --autoreload
```

The `--autoreload` flag automatically refreshes when you edit the code.

## 🐛 Troubleshooting

**Issue**: "No module named panel"
- **Solution**: Make sure you activated the conda environment: `conda activate condacarol`

**Issue**: "Address already in use"
- **Solution**: Change the port: `panel serve app.py --port 5007`

**Issue**: Can't access from other devices
- **Solution**: Use `--address 0.0.0.0` flag and check your firewall settings

**Issue**: Game state resets when page refreshes
- **Solution**: This is expected with in-memory storage. For persistence, implement JSON/database storage.

## 🤝 Contributing

Feel free to submit issues and enhancement requests!

## 📜 License

MIT License - feel free to use for your holiday parties!

## 🎅 Credits

Made with ❤️ using:
- [Panel](https://panel.holoviz.org/) - Python web framework
- [Anaconda](https://www.anaconda.com/) - Package management
- Christmas spirit ✨

---

**Merry Christmas and Happy Guessing!** 🎄🐍🎁
