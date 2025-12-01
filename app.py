"""
CondaCarol - A Christmas Party Guessing Game
Learn more about your colleagues through fun questions and guessing games!
"""

import panel as pn
import json

# Initialize Panel with custom CSS
pn.extension(design='material', notifications=True, raw_css=['''
:root {
  --color-primary: #43B02A;
  --color-bg: #0E1117;
  --color-surface: #1A1F2E;
  --color-surface-variant: #242938;
  --color-text: #FFFFFF;
  --color-text-muted: #8B92A7;
  --color-border: #2A2F3D;
  --color-warning: #FF9500;
  --color-error: #FF3B30;
  --spacing-unit: 8px;
  --radius-sm: 6px;
  --radius-md: 8px;
  --transition-fast: 150ms cubic-bezier(0.4, 0.0, 0.2, 1);
}

body {
  background: var(--color-bg) !important;
  color: var(--color-text) !important;
  font-family: 'Inter Variable', system-ui, -apple-system, sans-serif !important;
  background-image: radial-gradient(circle at 20% 30%, rgba(67, 176, 42, 0.03) 0%, transparent 50%) !important;
}

.bk-root {
  background: transparent !important;
}

/* Card styling */
.card {
  background: var(--color-surface) !important;
  border: 1px solid var(--color-border) !important;
  border-radius: var(--radius-md) !important;
  padding: 24px !important;
  margin-bottom: 24px !important;
  transition: all var(--transition-fast) !important;
}

.card:hover {
  border-color: rgba(67, 176, 42, 0.3) !important;
}

/* Button overrides */
.bk-btn-primary {
  background-color: var(--color-primary) !important;
  border: none !important;
  color: white !important;
  border-radius: var(--radius-sm) !important;
  font-weight: 500 !important;
  padding: 12px 24px !important;
  transition: all var(--transition-fast) !important;
}

.bk-btn-primary:hover {
  filter: brightness(110%) !important;
  transform: translateY(-1px) !important;
}

.bk-btn-success {
  background-color: var(--color-primary) !important;
  border: none !important;
  color: white !important;
  border-radius: var(--radius-sm) !important;
  font-weight: 500 !important;
  padding: 12px 24px !important;
}

.bk-btn-danger {
  background-color: var(--color-error) !important;
  border: none !important;
  border-radius: var(--radius-sm) !important;
}

.bk-btn-default {
  background: transparent !important;
  border: 1px solid var(--color-border) !important;
  color: var(--color-text) !important;
  border-radius: var(--radius-sm) !important;
  transition: all var(--transition-fast) !important;
}

.bk-btn-default:hover {
  border-color: var(--color-primary) !important;
  background: rgba(67, 176, 42, 0.05) !important;
}

.bk-btn-warning {
  background-color: var(--color-warning) !important;
  border: none !important;
  border-radius: var(--radius-sm) !important;
}

/* Input fields - Comprehensive coverage */
input, textarea, select, .bk-input, .bk-input-group input {
  background: var(--color-surface-variant) !important;
  border: 1px solid var(--color-border) !important;
  color: var(--color-text) !important;
  border-radius: var(--radius-sm) !important;
  padding: 12px !important;
  transition: all var(--transition-fast) !important;
}

input::placeholder, textarea::placeholder {
  color: var(--color-text-muted) !important;
  opacity: 0.6 !important;
}

input:focus, textarea:focus, select:focus, .bk-input:focus {
  border-color: var(--color-primary) !important;
  outline: none !important;
  box-shadow: 0 0 0 2px rgba(67, 176, 42, 0.1) !important;
}

/* Password inputs */
input[type="password"] {
  background: var(--color-surface-variant) !important;
  color: var(--color-text) !important;
}

/* Text inputs */
input[type="text"] {
  background: var(--color-surface-variant) !important;
  color: var(--color-text) !important;
}

/* TextArea */
textarea, .bk-input-group textarea {
  background: var(--color-surface-variant) !important;
  color: var(--color-text) !important;
  font-family: 'Inter Variable', system-ui, -apple-system, sans-serif !important;
}

/* Select dropdowns - Multiple selectors for coverage */
select, select.bk-input, .bk-input-group select {
  background: var(--color-surface-variant) !important;
  border: 1px solid var(--color-border) !important;
  color: var(--color-text) !important;
  border-radius: var(--radius-sm) !important;
  padding: 12px !important;
}

/* Dropdown options */
select option, select.bk-input option {
  background: var(--color-surface-variant) !important;
  color: var(--color-text) !important;
  padding: 8px !important;
}

/* Disabled inputs */
input:disabled, textarea:disabled, select:disabled, .bk-input:disabled {
  opacity: 0.6 !important;
  cursor: not-allowed !important;
  background: var(--color-surface) !important;
  color: var(--color-text-muted) !important;
}

/* Radio buttons and RadioButtonGroup */
input[type="radio"] {
  accent-color: var(--color-primary) !important;
  width: 18px !important;
  height: 18px !important;
  margin-right: 8px !important;
}

.bk-btn-group {
  display: flex !important;
  flex-direction: column !important;
  gap: 8px !important;
  width: 100% !important;
}

.bk-btn-group .bk-btn {
  background: var(--color-surface-variant) !important;
  border: 1px solid var(--color-border) !important;
  color: var(--color-text) !important;
  text-align: left !important;
  padding: 12px 16px !important;
  border-radius: var(--radius-sm) !important;
  transition: all var(--transition-fast) !important;
  font-weight: 400 !important;
  margin: 0 !important;
  width: 100% !important;
}

.bk-btn-group .bk-btn:hover {
  border-color: var(--color-primary) !important;
  background: rgba(67, 176, 42, 0.08) !important;
  transform: translateX(4px) !important;
}

.bk-btn-group .bk-btn.bk-active {
  background: rgba(67, 176, 42, 0.15) !important;
  border-color: var(--color-primary) !important;
  color: var(--color-text) !important;
  font-weight: 500 !important;
  box-shadow: 0 0 0 2px rgba(67, 176, 42, 0.2) !important;
}

.answer-card {
  background: var(--color-surface-variant) !important;
  border: 1px solid var(--color-border) !important;
  border-radius: var(--radius-md) !important;
  padding: 20px !important;
  margin-bottom: 24px !important;
}

/* Labels - Comprehensive - Positioned ABOVE inputs */
label, .bk-label, .bk-input-label, legend {
  color: var(--color-text) !important;
  font-weight: 500 !important;
  margin-bottom: 8px !important;
  margin-top: 0 !important;
  background: transparent !important;
  display: block !important;
  position: relative !important;
  width: 100% !important;
}

/* Ensure labels are above their inputs, not overlapping */
.bk-input-group > label,
.bk-input-container > label {
  display: block !important;
  margin-bottom: 8px !important;
  position: static !important;
}

/* Input wrapper positioning */
.bk-input-group,
.bk-input-container {
  display: flex !important;
  flex-direction: column !important;
  gap: 0 !important;
}

/* Widget containers */
.bk-input-group, .bk-widget-form-group {
  background: transparent !important;
}

/* Panel panes */
.bk-panel-models-markup-HTML, .bk-panel-models-markup-Markdown {
  background: transparent !important;
  color: var(--color-text) !important;
}

/* Ensure all text is visible - More specific */
.bk p, .bk span, .bk div, .bk-root p, .bk-root span, .bk-root div {
  color: var(--color-text) !important;
}

/* Force all bokeh elements to have proper text color */
.bk, .bk-root, .bk * {
  color: var(--color-text);
}

/* Input widget specific fixes */
.bk-input-container input,
.bk-input-container textarea,
.bk-input-container select {
  background: var(--color-surface-variant) !important;
  color: var(--color-text) !important;
  border: 1px solid var(--color-border) !important;
}

/* Widget labels inside forms */
.bk-input-group label,
.bk-input-container label {
  color: var(--color-text) !important;
  background: transparent !important;
}

/* Widget boxes */
.bk-widget-box {
  background: transparent !important;
}

/* Tabs */
.bk-tab {
  background: var(--color-surface) !important;
  border: 1px solid var(--color-border) !important;
  color: var(--color-text-muted) !important;
  border-radius: var(--radius-sm) var(--radius-sm) 0 0 !important;
  padding: 12px 24px !important;
  transition: all var(--transition-fast) !important;
}

.bk-tab.bk-active {
  background: var(--color-bg) !important;
  color: var(--color-primary) !important;
  border-bottom-color: transparent !important;
  font-weight: 600 !important;
}

.bk-tab:hover {
  background: var(--color-surface-variant) !important;
  color: var(--color-text) !important;
}

/* Dividers */
hr {
  border-color: var(--color-border) !important;
  margin: 32px 0 !important;
}

/* Markdown content */
.markdown {
  color: var(--color-text) !important;
}

.markdown h1, .markdown h2, .markdown h3 {
  color: var(--color-text) !important;
  font-weight: 600 !important;
}

.markdown h1 {
  font-size: 32px !important;
  margin-bottom: 24px !important;
}

.markdown h2 {
  font-size: 24px !important;
  margin-bottom: 16px !important;
  margin-top: 32px !important;
}

.markdown h3 {
  font-size: 20px !important;
  margin-bottom: 12px !important;
  margin-top: 24px !important;
}

.markdown p {
  color: var(--color-text-muted) !important;
  line-height: 1.6 !important;
}

.markdown strong {
  color: var(--color-text) !important;
  font-weight: 600 !important;
}

.markdown code {
  background: var(--color-surface-variant) !important;
  color: var(--color-primary) !important;
  padding: 2px 6px !important;
  border-radius: 4px !important;
  font-family: 'JetBrains Mono', 'Fira Code', monospace !important;
}

/* Notification positioning */
.bk-notification {
  border-radius: var(--radius-sm) !important;
  padding: 16px !important;
}

/* Christmas theming accents */
.christmas-accent {
  background: linear-gradient(135deg, #43B02A 0%, #2d7a1c 100%) !important;
}

/* Phase indicator */
.phase-indicator {
  background: var(--color-surface) !important;
  border: 1px solid var(--color-border) !important;
  border-radius: var(--radius-md) !important;
  padding: 16px 24px !important;
  margin-bottom: 24px !important;
}

/* Emoji styling */
.emoji {
  font-size: 24px !important;
}
'''])

# Global state to store game data - now organized by city
game_state = {
    'cities': {},  # {city_name: {questions, answers, guesses, participants, phase}}
    'admin_password': 'condaclaus2024'
}

# Helper function to get or create city data
def get_city_data(city_name):
    if city_name not in game_state['cities']:
        game_state['cities'][city_name] = {
            'questions': [],
            'answers': {},  # {participant_name: {question_id: answer}}
            'guesses': {},  # {guesser_name: {question_id: {answer_id: guessed_name}}}
            'participants': set(),
            'phase': 'setup'  # setup, answer, game, results
        }
    return game_state['cities'][city_name]

# Session state to track logged-in user (per browser session)
if 'user_session' not in pn.state.cache:
    pn.state.cache['user_session'] = {
        'username': None,
        'city': None,
        'is_admin': False,
        'logged_in': False
    }


def create_login_view():
    """Login screen for all users (participants and admin)"""
    title = pn.pane.Markdown(
        "# 🎄 Welcome to CondaCarol! 🐍",
        sizing_mode='stretch_width',
        styles={'text-align': 'center'}
    )

    subtitle = pn.pane.Markdown(
        """
        **A Christmas Party Guessing Game**

        Learn more about your colleagues through fun questions and guess who said what!
        """,
        sizing_mode='stretch_width',
        styles={'text-align': 'center', 'color': '#8B92A7'}
    )

    # Participant login section
    participant_section = pn.Column(sizing_mode='stretch_width')
    participant_section.append(pn.pane.Markdown("## 🎁 Join as Participant", sizing_mode='stretch_width'))

    # Get list of available cities
    available_cities = list(game_state['cities'].keys())

    name_input = pn.widgets.TextInput(
        name='',
        placeholder='Enter your name',
        width=400
    )

    city_select = pn.widgets.Select(
        name='',
        options=['-- Select City --'] + available_cities if available_cities else ['-- No cities available --'],
        value='-- Select City --' if available_cities else '-- No cities available --',
        width=400,
        disabled=len(available_cities) == 0
    )

    name_label = pn.pane.Markdown("**Your Name:**", sizing_mode='stretch_width')
    city_label = pn.pane.Markdown("**Your City/Office:**", sizing_mode='stretch_width')

    if not available_cities:
        no_cities_msg = pn.pane.Markdown(
            "*⚠️ No cities available yet. An admin needs to create a city first.*",
            sizing_mode='stretch_width',
            styles={'color': '#FF9500'}
        )
    else:
        no_cities_msg = pn.Spacer(height=0)

    def participant_login(event):
        username = name_input.value.strip()
        selected_city = city_select.value

        if not username:
            pn.state.notifications.error('❌ Please enter your name!', duration=3000)
            return

        if not available_cities:
            pn.state.notifications.error('❌ No cities available! Contact an admin.', duration=4000)
            return

        if selected_city.startswith('--'):
            pn.state.notifications.error('❌ Please select your city!', duration=3000)
            return

        pn.state.cache['user_session'] = {
            'username': username,
            'city': selected_city,
            'is_admin': False,
            'logged_in': True
        }
        pn.state.notifications.success(f'🎉 Welcome, {username} from {selected_city}!', duration=3000)
        # Force a refresh to show the main app
        pn.state.location.reload = True

    participant_btn = pn.widgets.Button(
        name='🎮 Join Game',
        button_type='primary',
        width=200
    )
    participant_btn.on_click(participant_login)

    participant_section.append(no_cities_msg)
    participant_section.append(pn.Spacer(height=12))
    participant_section.append(name_label)
    participant_section.append(name_input)
    participant_section.append(pn.Spacer(height=12))
    participant_section.append(city_label)
    participant_section.append(city_select)
    participant_section.append(pn.Spacer(height=16))
    participant_section.append(participant_btn)

    # Admin login section
    admin_section = pn.Column(sizing_mode='stretch_width')
    admin_section.append(pn.layout.Divider())
    admin_section.append(pn.Spacer(height=24))
    admin_section.append(pn.pane.Markdown("## 🔑 Admin Login", sizing_mode='stretch_width'))

    admin_name_input = pn.widgets.TextInput(
        name='',
        placeholder='Admin name',
        width=400
    )

    admin_password_input = pn.widgets.PasswordInput(
        name='',
        placeholder='Admin password',
        width=400
    )

    # City options for admin
    admin_city_options = ['-- Create New City --'] + available_cities if available_cities else ['-- Create New City --']
    admin_city_select = pn.widgets.Select(
        name='',
        options=admin_city_options,
        value='-- Create New City --',
        width=400
    )

    new_city_input = pn.widgets.TextInput(
        name='',
        placeholder='Enter new city name (e.g., San Francisco)',
        width=400,
        visible=True
    )

    def on_admin_city_change(event):
        if admin_city_select.value == '-- Create New City --':
            new_city_input.visible = True
        else:
            new_city_input.visible = False

    admin_city_select.param.watch(on_admin_city_change, 'value')

    admin_name_label = pn.pane.Markdown("**Admin Name:**", sizing_mode='stretch_width')
    admin_password_label = pn.pane.Markdown("**Password:**", sizing_mode='stretch_width')
    admin_city_label = pn.pane.Markdown("**City/Office:**", sizing_mode='stretch_width')

    def admin_login(event):
        username = admin_name_input.value.strip()
        password = admin_password_input.value

        if not username:
            pn.state.notifications.error('❌ Please enter your name!', duration=3000)
            return

        if password != game_state['admin_password']:
            pn.state.notifications.error('❌ Incorrect admin password!', duration=3000)
            return

        # Determine city
        if admin_city_select.value == '-- Create New City --':
            city_name = new_city_input.value.strip()
            if not city_name:
                pn.state.notifications.error('❌ Please enter a city name!', duration=3000)
                return
            # Create new city
            get_city_data(city_name)
            pn.state.notifications.info(f'🏙️ Created new city: {city_name}', duration=3000)
        else:
            city_name = admin_city_select.value

        pn.state.cache['user_session'] = {
            'username': username,
            'city': city_name,
            'is_admin': True,
            'logged_in': True
        }
        pn.state.notifications.success(f'🎉 Welcome Admin {username} ({city_name})!', duration=3000)
        # Force a refresh to show the main app
        pn.state.location.reload = True

    admin_btn = pn.widgets.Button(
        name='🔐 Login as Admin',
        button_type='success',
        width=200
    )
    admin_btn.on_click(admin_login)

    admin_section.append(admin_name_label)
    admin_section.append(admin_name_input)
    admin_section.append(pn.Spacer(height=12))
    admin_section.append(admin_password_label)
    admin_section.append(admin_password_input)
    admin_section.append(pn.Spacer(height=12))
    admin_section.append(admin_city_label)
    admin_section.append(admin_city_select)
    admin_section.append(pn.Spacer(height=8))
    admin_section.append(new_city_input)
    admin_section.append(pn.Spacer(height=16))
    admin_section.append(admin_btn)

    return pn.Column(
        pn.Spacer(height=48),
        title,
        subtitle,
        pn.Spacer(height=48),
        participant_section,
        admin_section,
        pn.Spacer(height=48),
        sizing_mode='stretch_width',
        max_width=600,
        styles={'margin': '0 auto'},
        css_classes=['card']
    )


def create_setup_view():
    """Admin view to set up questions"""
    city = pn.state.cache['user_session']['city']
    city_data = get_city_data(city)

    title = pn.pane.Markdown(f"# 🎄 Setup Questions - {city}", sizing_mode='stretch_width', css_classes=['christmas-header'])
    instructions = pn.pane.Markdown("""
    **Admin Setup**: Add questions for participants to answer.
    These should be fun, personal questions that help everyone learn about each other!

    Example questions:
    - What's your most embarrassing childhood memory?
    - If you could have dinner with anyone, who would it be?
    - What's your hidden talent?
    """, sizing_mode='stretch_width')

    question_input = pn.widgets.TextAreaInput(
        name='New Question',
        placeholder='e.g., What was your favorite vacation destination?',
        height=100,
        width=600
    )

    questions_list = pn.widgets.TextAreaInput(
        name='Current Questions',
        value='No questions added yet.',
        height=250,
        disabled=True,
        width=600
    )

    def update_questions_display():
        if city_data['questions']:
            questions_text = '\n\n'.join([
                f"{i+1}. {q}" for i, q in enumerate(city_data['questions'])
            ])
        else:
            questions_text = 'No questions added yet.'
        questions_list.value = questions_text

    def add_question(event):
        if question_input.value.strip():
            city_data['questions'].append(question_input.value.strip())
            pn.state.notifications.success(f'✅ Question added! Total: {len(city_data["questions"])}', duration=3000)
            question_input.value = ''
            update_questions_display()
        else:
            pn.state.notifications.warning('⚠️ Please enter a question.', duration=3000)

    def clear_questions(event):
        city_data['questions'] = []
        city_data['answers'] = {}
        pn.state.notifications.info('🗑️ All questions cleared!', duration=3000)
        update_questions_display()

    def start_answer_phase(event):
        if len(city_data['questions']) < 3:
            pn.state.notifications.error('❌ Please add at least 3 questions!', duration=3000)
            return

        city_data['phase'] = 'answer'
        pn.state.notifications.success(
            '🎉 Answer phase started! Tell participants to go to the "Answer" tab and click "Refresh Questions".',
            duration=8000
        )

    add_btn = pn.widgets.Button(name='➕ Add Question', button_type='primary', width=180)
    add_btn.on_click(add_question)

    clear_btn = pn.widgets.Button(name='🗑️ Clear All', button_type='danger', width=150)
    clear_btn.on_click(clear_questions)

    start_btn = pn.widgets.Button(name='▶️ Start Answer Phase', button_type='success', width=220, css_classes=['christmas-accent'])
    start_btn.on_click(start_answer_phase)

    return pn.Column(
        title,
        instructions,
        pn.Spacer(height=24),
        question_input,
        pn.Spacer(height=16),
        pn.Row(add_btn, pn.Spacer(width=16), clear_btn),
        pn.Spacer(height=24),
        questions_list,
        pn.Spacer(height=24),
        start_btn,
        sizing_mode='stretch_width',
        css_classes=['card']
    )


def create_answer_view():
    """Participant view to answer questions"""
    city = pn.state.cache['user_session']['city']
    city_data = get_city_data(city)
    username = pn.state.cache['user_session']['username']

    title = pn.pane.Markdown(f"# 🎁 {username}'s Answers", sizing_mode='stretch_width')
    instructions = pn.pane.Markdown("""
    **Answer the questions below**. Your answers will be shared anonymously during the guessing game!
    Be creative and have fun with your responses!

    **💡 Tip:** If questions don't appear, click the "Refresh Questions" button below.
    """, sizing_mode='stretch_width')

    status_message = pn.pane.Markdown(
        "",
        sizing_mode='stretch_width',
        styles={'padding': '12px', 'background': 'rgba(67, 176, 42, 0.1)', 'border-radius': '6px', 'border': '1px solid #43B02A'}
    )

    answers_column = pn.Column(sizing_mode='stretch_width')
    answer_widgets = []

    def update_answer_form(event=None):
        answer_widgets.clear()
        answers_column.clear()

        if not city_data['questions']:
            answers_column.append(pn.pane.Markdown('*⏳ Waiting for admin to add questions...*'))
            status_message.object = "**📢 No questions yet.** The admin needs to add questions in the Setup tab first."
            return

        # Show status message
        status_message.object = f"**✅ {len(city_data['questions'])} questions loaded!** Fill out your answers below."

        for i, question in enumerate(city_data['questions']):
            # Add question label separately for better styling
            question_label = pn.pane.Markdown(
                f"**Question {i+1}:** {question}",
                sizing_mode='stretch_width',
                styles={'margin-bottom': '8px', 'margin-top': '16px'}
            )
            answers_column.append(question_label)

            widget = pn.widgets.TextAreaInput(
                name='',  # Empty name since we have the label above
                placeholder='Type your answer here...',
                height=80,
                width=600
            )
            answer_widgets.append(widget)
            answers_column.append(widget)
            answers_column.append(pn.Spacer(height=8))

    def submit_answers(event):
        participant_name = username

        if participant_name in city_data['answers']:
            pn.state.notifications.warning('⚠️ You have already submitted answers!', duration=3000)
            return

        if not answer_widgets:
            pn.state.notifications.error('❌ No questions available yet!', duration=3000)
            return

        answers = {}
        for i, widget in enumerate(answer_widgets):
            if not widget.value.strip():
                pn.state.notifications.error(f'❌ Please answer question {i+1}!', duration=3000)
                return
            answers[i] = widget.value.strip()

        city_data['answers'][participant_name] = answers
        city_data['participants'].add(participant_name)
        pn.state.notifications.success(f'🎉 Thanks {participant_name}! Your answers have been submitted.', duration=5000)

        # Clear answers for re-submission if needed
        for widget in answer_widgets:
            widget.value = ''

    submit_btn = pn.widgets.Button(name='✅ Submit Answers', button_type='primary', width=200)
    submit_btn.on_click(submit_answers)

    refresh_btn = pn.widgets.Button(name='🔄 Refresh Questions', button_type='success', width=250)
    refresh_btn.on_click(update_answer_form)

    participants_info = pn.pane.Markdown(
        f"**👥 Participants**: {len(city_data['participants'])} people have submitted answers",
        sizing_mode='stretch_width'
    )

    update_answer_form()

    return pn.Column(
        title,
        instructions,
        pn.Spacer(height=16),
        pn.pane.Markdown("**👇 Click this button first to load questions:**", sizing_mode='stretch_width'),
        refresh_btn,
        pn.Spacer(height=16),
        status_message,
        pn.Spacer(height=24),
        answers_column,
        pn.Spacer(height=24),
        submit_btn,
        pn.layout.Divider(),
        participants_info,
        sizing_mode='stretch_width',
        css_classes=['card']
    )


def create_game_view():
    """Game view where participants guess who said what"""
    city = pn.state.cache['user_session']['city']
    city_data = get_city_data(city)
    username = pn.state.cache['user_session']['username']

    title = pn.pane.Markdown(f"# 🎅 {username}'s Guesses", sizing_mode='stretch_width')
    instructions = pn.pane.Markdown("""
    **Match each answer to the person who said it!**
    Each person can only be matched once per question.

    **💡 Tip:** Click "Refresh Game" button below to load the latest answers.
    """, sizing_mode='stretch_width')

    guesses_column = pn.Column(sizing_mode='stretch_width')
    # Store widgets per question to prevent clearing issues
    all_guess_widgets = {}

    def create_question_section(q_idx, question):
        """Create a section for matching answers to participants for one question"""
        section = pn.Column(sizing_mode='stretch_width')

        section.append(pn.pane.Markdown(f"### 🎯 Question {q_idx+1}: {question}", sizing_mode='stretch_width'))
        section.append(pn.Spacer(height=16))

        # Get all answers for this question
        answers_for_question = []
        for participant, answers in city_data['answers'].items():
            if q_idx in answers:
                answers_for_question.append({
                    'participant': participant,
                    'answer': answers[q_idx]
                })

        if not answers_for_question:
            section.append(pn.pane.Markdown('*No answers for this question*'))
            return section

        participant_list = sorted(list(city_data['participants']))

        # Create matching interface for this question
        instructions_md = pn.pane.Markdown(
            f"**Match the {len(answers_for_question)} answers below to the participants:**",
            sizing_mode='stretch_width'
        )
        section.append(instructions_md)
        section.append(pn.Spacer(height=16))

        # Create widgets for each answer
        for a_idx, ans_data in enumerate(answers_for_question):
            # Create card for each answer
            answer_card = pn.Column(sizing_mode='stretch_width', css_classes=['answer-card'])

            answer_text = pn.pane.Markdown(
                f"**Answer {a_idx + 1}:** *\"{ans_data['answer']}\"*",
                sizing_mode='stretch_width'
            )

            selection_label = pn.pane.Markdown(
                "**Who said this?**",
                sizing_mode='stretch_width',
                styles={'margin-top': '12px', 'margin-bottom': '8px'}
            )

            # Use RadioButtonGroup for better UX
            guess_select = pn.widgets.RadioButtonGroup(
                name='',  # Empty name - we have our own label above
                options=participant_list,
                button_type='default',
                button_style='outline',
                orientation='vertical',
                width=400
            )

            key = f'q{q_idx}_a{a_idx}'
            all_guess_widgets[key] = {
                'widget': guess_select,
                'correct_answer': ans_data['participant'],
                'q_idx': q_idx
            }

            answer_card.append(answer_text)
            answer_card.append(selection_label)
            answer_card.append(guess_select)

            section.append(answer_card)
            section.append(pn.Spacer(height=16))

        return section

    def update_game_form(event=None):
        guesses_column.clear()
        all_guess_widgets.clear()

        if not city_data['answers']:
            guesses_column.append(pn.pane.Markdown('*⏳ No answers submitted yet...*'))
            return

        # Create sections for each question
        for q_idx, question in enumerate(city_data['questions']):
            section = create_question_section(q_idx, question)
            guesses_column.append(section)
            guesses_column.append(pn.layout.Divider())

    def validate_guesses():
        """Check if all answers are matched and no duplicates per question"""
        # Group by question
        questions_guesses = {}
        for key, data in all_guess_widgets.items():
            q_idx = data['q_idx']
            if q_idx not in questions_guesses:
                questions_guesses[q_idx] = []

            if data['widget'].value is None:
                return False, f"❌ Please match all answers for Question {q_idx + 1}!"

            questions_guesses[q_idx].append(data['widget'].value)

        # Check for duplicates per question
        for q_idx, guesses in questions_guesses.items():
            if len(guesses) != len(set(guesses)):
                return False, f"❌ You selected the same person twice for Question {q_idx + 1}! Each person can only be matched once per question."

        return True, ""

    def submit_guesses(event):
        guesser_name = username

        if not all_guess_widgets:
            pn.state.notifications.error('❌ No guesses available! Click Refresh Game first.', duration=3000)
            return

        # Validate all guesses
        valid, error_msg = validate_guesses()
        if not valid:
            pn.state.notifications.error(error_msg, duration=4000)
            return

        # Store guesses
        if guesser_name not in city_data['guesses']:
            city_data['guesses'][guesser_name] = {}

        for key, data in all_guess_widgets.items():
            city_data['guesses'][guesser_name][key] = {
                'guessed': data['widget'].value,
                'correct': data['correct_answer']
            }

        pn.state.notifications.success(f'🎉 Thanks {guesser_name}! Your guesses have been submitted.', duration=5000)

        # Clear form for re-submission if needed
        for data in all_guess_widgets.values():
            data['widget'].value = None

    submit_guess_btn = pn.widgets.Button(name='✅ Submit All Guesses', button_type='primary', width=220)
    submit_guess_btn.on_click(submit_guesses)

    refresh_btn = pn.widgets.Button(name='🔄 Refresh Game', button_type='success', width=200)
    refresh_btn.on_click(update_game_form)

    # Initial load
    update_game_form()

    return pn.Column(
        title,
        instructions,
        pn.Spacer(height=16),
        pn.pane.Markdown("**👇 Click this button first to load answers:**", sizing_mode='stretch_width'),
        refresh_btn,
        pn.Spacer(height=24),
        guesses_column,
        pn.Spacer(height=24),
        submit_guess_btn,
        sizing_mode='stretch_width',
        css_classes=['card']
    )


def create_results_view():
    """Results view showing scores and correct answers"""
    city = pn.state.cache['user_session']['city']
    city_data = get_city_data(city)
    title = pn.pane.Markdown("# 🎉 CondaCarol - Results!", sizing_mode='stretch_width')

    results_column = pn.Column(sizing_mode='stretch_width')

    def update_results(event=None):
        results_column.clear()

        if not city_data['guesses']:
            results_column.append(pn.pane.Markdown('*⏳ No guesses to show yet...*'))
            return

        scores = {}
        for guesser, guesses in city_data['guesses'].items():
            correct_count = 0
            total_count = len(guesses)

            for guess_data in guesses.values():
                if guess_data['guessed'] == guess_data['correct']:
                    correct_count += 1

            scores[guesser] = {
                'correct': correct_count,
                'total': total_count,
                'percentage': round((correct_count / total_count * 100), 1) if total_count > 0 else 0
            }

        sorted_scores = sorted(scores.items(), key=lambda x: x[1]['correct'], reverse=True)

        leaderboard_md = "## 🏆 Leaderboard\n\n"
        for i, (name, score_data) in enumerate(sorted_scores, 1):
            medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"**{i}.**"
            leaderboard_md += f"{medal} **{name}**: {score_data['correct']}/{score_data['total']} correct ({score_data['percentage']}%)\n\n"

        results_column.append(pn.pane.Markdown(leaderboard_md))
        results_column.append(pn.layout.Divider())

        results_column.append(pn.pane.Markdown("## 🎁 All Answers Revealed"))
        results_column.append(pn.Spacer(height=16))

        for q_idx, question in enumerate(city_data['questions']):
            results_column.append(pn.pane.Markdown(f"### Question {q_idx+1}: {question}"))

            for participant, answers in sorted(city_data['answers'].items()):
                if q_idx in answers:
                    results_column.append(pn.pane.Markdown(f"- **{participant}**: *\"{answers[q_idx]}\"*"))

            results_column.append(pn.Spacer(height=24))

    refresh_btn = pn.widgets.Button(name='🔄 Refresh Results', button_type='default', width=200)
    refresh_btn.on_click(update_results)

    update_results()

    return pn.Column(
        title,
        pn.Spacer(height=24),
        refresh_btn,
        pn.Spacer(height=24),
        results_column,
        sizing_mode='stretch_width',
        css_classes=['card']
    )


# Create the main app layout
def create_app():
    session = pn.state.cache['user_session']

    # If not logged in, show login screen
    if not session['logged_in']:
        return create_login_view()

    # User is logged in - show main app
    username = session['username']
    is_admin = session['is_admin']

    header = pn.pane.Markdown(
        "# 🐍 CondaCarol - Christmas Party Game 🎄",
        sizing_mode='stretch_width',
        styles={'text-align': 'center', 'font-size': '36px', 'margin-bottom': '16px'}
    )

    # User info and logout
    def logout(event):
        pn.state.cache['user_session'] = {
            'username': None,
            'is_admin': False,
            'logged_in': False
        }
        pn.state.notifications.info('👋 Logged out successfully!', duration=3000)
        pn.state.location.reload = True

    logout_btn = pn.widgets.Button(
        name='🚪 Logout',
        button_type='warning',
        width=120
    )
    logout_btn.on_click(logout)

    role_badge = "🔑 Admin" if is_admin else "🎮 Participant"
    user_info = pn.Row(
        pn.pane.Markdown(
            f"**{role_badge}** Logged in as: **{username}**",
            sizing_mode='stretch_width',
            styles={'text-align': 'center'}
        ),
        logout_btn,
        sizing_mode='stretch_width'
    )

    city = session['city']
    city_data = get_city_data(city)

    phase_info = pn.pane.Markdown(
        f"**🏙️ City:** `{city}` | "
        f"**Current Phase:** `{city_data['phase'].title()}` | "
        f"**👥 Participants:** `{len(city_data['participants'])}` | "
        f"**❓ Questions:** `{len(city_data['questions'])}`",
        sizing_mode='stretch_width',
        styles={'text-align': 'center', 'margin-bottom': '24px'},
        css_classes=['phase-indicator']
    )

    # Show different tabs based on role
    if is_admin:
        tabs = pn.Tabs(
            ('🎅 Setup', create_setup_view()),
            ('🎁 Answer', create_answer_view()),
            ('🎮 Play', create_game_view()),
            ('🏆 Results', create_results_view()),
            sizing_mode='stretch_width',
            margin=(24, 0)
        )
    else:
        # Participants only see Answer, Play, and Results tabs
        tabs = pn.Tabs(
            ('🎁 Answer', create_answer_view()),
            ('🎮 Play', create_game_view()),
            ('🏆 Results', create_results_view()),
            sizing_mode='stretch_width',
            margin=(24, 0)
        )

    return pn.Column(
        pn.Spacer(height=24),
        header,
        user_info,
        pn.Spacer(height=24),
        phase_info,
        tabs,
        pn.Spacer(height=48),
        sizing_mode='stretch_width',
        max_width=1200,
        styles={'margin': '0 auto'}
    )


# Serve the app
create_app().servable()
