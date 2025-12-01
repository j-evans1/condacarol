"""
CondaCarol - A Christmas Party Guessing Game
Learn more about your colleagues through fun questions and guessing games!
"""

import panel as pn
import json

# Initialize Panel
pn.extension(design='material', notifications=True)

# Global state to store game data
game_state = {
    'questions': [],
    'answers': {},  # {participant_name: {question_id: answer}}
    'guesses': {},  # {guesser_name: {question_id: {answer_id: guessed_name}}}
    'participants': set(),
    'phase': 'setup',  # setup, answer, game, results
    'admin_password': 'condaclaus2024'
}


def create_setup_view():
    """Admin view to set up questions"""
    title = pn.pane.Markdown("# 🎄 CondaCarol - Setup Questions 🎅", sizing_mode='stretch_width')
    instructions = pn.pane.Markdown("""
    **Admin Setup**: Add questions for participants to answer.
    These should be fun, personal questions that help everyone learn about each other!
    """, sizing_mode='stretch_width')

    password_input = pn.widgets.PasswordInput(
        name='Admin Password',
        placeholder='Enter admin password'
    )

    question_input = pn.widgets.TextAreaInput(
        name='Question',
        placeholder='e.g., What was your favorite vacation destination?',
        height=100
    )

    questions_list = pn.widgets.TextAreaInput(
        name='Current Questions',
        value='No questions added yet.',
        height=200,
        disabled=True
    )

    def update_questions_display():
        if game_state['questions']:
            questions_text = '\n\n'.join([
                f"{i+1}. {q}" for i, q in enumerate(game_state['questions'])
            ])
        else:
            questions_text = 'No questions added yet.'
        questions_list.value = questions_text

    def add_question(event):
        if password_input.value != game_state['admin_password']:
            pn.state.notifications.error('Incorrect admin password!', duration=3000)
            return

        if question_input.value.strip():
            game_state['questions'].append(question_input.value.strip())
            pn.state.notifications.success(f'Question added! Total: {len(game_state["questions"])}', duration=3000)
            question_input.value = ''
            update_questions_display()
        else:
            pn.state.notifications.warning('Please enter a question.', duration=3000)

    def clear_questions(event):
        if password_input.value != game_state['admin_password']:
            pn.state.notifications.error('Incorrect admin password!', duration=3000)
            return

        game_state['questions'] = []
        game_state['answers'] = {}
        pn.state.notifications.info('All questions cleared!', duration=3000)
        update_questions_display()

    def start_answer_phase(event):
        if password_input.value != game_state['admin_password']:
            pn.state.notifications.error('Incorrect admin password!', duration=3000)
            return

        if len(game_state['questions']) < 3:
            pn.state.notifications.error('Please add at least 3 questions!', duration=3000)
            return

        game_state['phase'] = 'answer'
        pn.state.notifications.success('Answer phase started! Share the link with participants.', duration=5000)

    add_btn = pn.widgets.Button(name='Add Question', button_type='primary', width=150)
    add_btn.on_click(add_question)

    clear_btn = pn.widgets.Button(name='Clear All Questions', button_type='danger', width=150)
    clear_btn.on_click(clear_questions)

    start_btn = pn.widgets.Button(name='Start Answer Phase →', button_type='success', width=200)
    start_btn.on_click(start_answer_phase)

    return pn.Column(
        title,
        instructions,
        password_input,
        question_input,
        pn.Row(add_btn, clear_btn),
        questions_list,
        start_btn,
        sizing_mode='stretch_width'
    )


def create_answer_view():
    """Participant view to answer questions"""
    title = pn.pane.Markdown("# 🎁 CondaCarol - Answer Questions 🎄", sizing_mode='stretch_width')
    instructions = pn.pane.Markdown("""
    **Answer the questions below**. Your answers will be shared anonymously during the guessing game!
    """, sizing_mode='stretch_width')

    name_input = pn.widgets.TextInput(
        name='Your Name',
        placeholder='Enter your name'
    )

    answers_column = pn.Column(sizing_mode='stretch_width')
    answer_widgets = []

    def update_answer_form(event=None):
        answer_widgets.clear()
        answers_column.clear()

        if not game_state['questions']:
            answers_column.append(pn.pane.Markdown('*Waiting for admin to add questions...*'))
            return

        for i, question in enumerate(game_state['questions']):
            widget = pn.widgets.TextAreaInput(
                name=f'Q{i+1}: {question}',
                placeholder='Your answer...',
                height=80
            )
            answer_widgets.append(widget)
            answers_column.append(widget)

    def submit_answers(event):
        if not name_input.value.strip():
            pn.state.notifications.error('Please enter your name!', duration=3000)
            return

        participant_name = name_input.value.strip()

        if participant_name in game_state['answers']:
            pn.state.notifications.warning('You have already submitted answers!', duration=3000)
            return

        if not answer_widgets:
            pn.state.notifications.error('No questions available yet!', duration=3000)
            return

        answers = {}
        for i, widget in enumerate(answer_widgets):
            if not widget.value.strip():
                pn.state.notifications.error(f'Please answer question {i+1}!', duration=3000)
                return
            answers[i] = widget.value.strip()

        game_state['answers'][participant_name] = answers
        game_state['participants'].add(participant_name)
        pn.state.notifications.success(f'Thanks {participant_name}! Your answers have been submitted.', duration=5000)

        name_input.value = ''
        for widget in answer_widgets:
            widget.value = ''

    submit_btn = pn.widgets.Button(name='Submit Answers', button_type='primary', width=150)
    submit_btn.on_click(submit_answers)

    refresh_btn = pn.widgets.Button(name='Refresh Questions', button_type='default', width=150)
    refresh_btn.on_click(update_answer_form)

    participants_text = pn.pane.Markdown(f"**Participants so far**: {len(game_state['participants'])}")

    update_answer_form()

    return pn.Column(
        title,
        instructions,
        name_input,
        refresh_btn,
        answers_column,
        submit_btn,
        pn.layout.Divider(),
        participants_text,
        sizing_mode='stretch_width'
    )


def create_game_view():
    """Game view where participants guess who said what"""
    title = pn.pane.Markdown("# 🎅 CondaCarol - Guess Who! 🎄", sizing_mode='stretch_width')
    instructions = pn.pane.Markdown("""
    **Read each answer and guess who wrote it!** Each correct guess earns you a point.
    """, sizing_mode='stretch_width')

    guesser_name_input = pn.widgets.TextInput(
        name='Your Name',
        placeholder='Enter your name to start guessing'
    )

    guesses_column = pn.Column(sizing_mode='stretch_width')
    guess_widgets = {}

    def update_game_form(event=None):
        guesses_column.clear()
        guess_widgets.clear()

        if not game_state['answers']:
            guesses_column.append(pn.pane.Markdown('*No answers submitted yet...*'))
            return

        participant_list = sorted(list(game_state['participants']))

        for q_idx, question in enumerate(game_state['questions']):
            guesses_column.append(pn.pane.Markdown(f"### Question {q_idx+1}: {question}"))

            answers_for_question = []
            for participant, answers in game_state['answers'].items():
                if q_idx in answers:
                    answers_for_question.append({
                        'participant': participant,
                        'answer': answers[q_idx]
                    })

            for a_idx, ans_data in enumerate(answers_for_question):
                answer_text = pn.pane.Markdown(f"**Answer:** *{ans_data['answer']}*")

                guess_select = pn.widgets.Select(
                    name=f'Who said this?',
                    options=['-- Select --'] + participant_list,
                    value='-- Select --'
                )

                guess_widgets[f'q{q_idx}_a{a_idx}'] = {
                    'widget': guess_select,
                    'correct_answer': ans_data['participant']
                }

                guesses_column.append(pn.Column(answer_text, guess_select))

            guesses_column.append(pn.layout.Divider())

    def submit_guesses(event):
        if not guesser_name_input.value.strip():
            pn.state.notifications.error('Please enter your name!', duration=3000)
            return

        if not guess_widgets:
            pn.state.notifications.error('No guesses available!', duration=3000)
            return

        for key, data in guess_widgets.items():
            if data['widget'].value == '-- Select --':
                pn.state.notifications.error('Please make all your guesses!', duration=3000)
                return

        guesser_name = guesser_name_input.value.strip()

        if guesser_name not in game_state['guesses']:
            game_state['guesses'][guesser_name] = {}

        for key, data in guess_widgets.items():
            game_state['guesses'][guesser_name][key] = {
                'guessed': data['widget'].value,
                'correct': data['correct_answer']
            }

        pn.state.notifications.success(f'Thanks {guesser_name}! Your guesses have been submitted.', duration=5000)
        guesser_name_input.value = ''
        for data in guess_widgets.values():
            data['widget'].value = '-- Select --'

    submit_guess_btn = pn.widgets.Button(name='Submit Guesses', button_type='primary', width=150)
    submit_guess_btn.on_click(submit_guesses)

    refresh_btn = pn.widgets.Button(name='Refresh Game', button_type='default', width=150)
    refresh_btn.on_click(update_game_form)

    update_game_form()

    return pn.Column(
        title,
        instructions,
        guesser_name_input,
        refresh_btn,
        guesses_column,
        submit_guess_btn,
        sizing_mode='stretch_width'
    )


def create_results_view():
    """Results view showing scores and correct answers"""
    title = pn.pane.Markdown("# 🎉 CondaCarol - Results! 🏆", sizing_mode='stretch_width')

    results_column = pn.Column(sizing_mode='stretch_width')

    def update_results(event=None):
        results_column.clear()

        if not game_state['guesses']:
            results_column.append(pn.pane.Markdown('*No guesses to show yet...*'))
            return

        scores = {}
        for guesser, guesses in game_state['guesses'].items():
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
            medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
            leaderboard_md += f"{medal} **{name}**: {score_data['correct']}/{score_data['total']} correct ({score_data['percentage']}%)\n"

        results_column.append(pn.pane.Markdown(leaderboard_md))
        results_column.append(pn.layout.Divider())

        results_column.append(pn.pane.Markdown("## 🎁 All Answers Revealed"))

        for q_idx, question in enumerate(game_state['questions']):
            results_column.append(pn.pane.Markdown(f"### Question {q_idx+1}: {question}"))

            for participant, answers in sorted(game_state['answers'].items()):
                if q_idx in answers:
                    results_column.append(pn.pane.Markdown(f"- **{participant}**: *{answers[q_idx]}*"))

            results_column.append(pn.layout.Divider())

    refresh_btn = pn.widgets.Button(name='Refresh Results', button_type='default', width=150)
    refresh_btn.on_click(update_results)

    update_results()

    return pn.Column(
        title,
        results_column,
        refresh_btn,
        sizing_mode='stretch_width'
    )


# Create the main app layout
def create_app():
    header = pn.pane.Markdown("# 🐍 CondaCarol - Christmas Party Game 🎄", sizing_mode='stretch_width')

    phase_info = pn.pane.Markdown(
        f"**Current Phase**: {game_state['phase'].title()} | "
        f"**Participants**: {len(game_state['participants'])} | "
        f"**Questions**: {len(game_state['questions'])}",
        sizing_mode='stretch_width'
    )

    tabs = pn.Tabs(
        ('🎅 Setup', create_setup_view()),
        ('🎁 Answer Questions', create_answer_view()),
        ('🎮 Play Game', create_game_view()),
        ('🏆 Results', create_results_view()),
        sizing_mode='stretch_width'
    )

    return pn.Column(
        header,
        phase_info,
        pn.layout.Divider(),
        tabs,
        sizing_mode='stretch_width'
    )


# Serve the app
create_app().servable()
