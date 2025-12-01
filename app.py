"""
CondaCarol - A Christmas Party Guessing Game
Learn more about your colleagues through fun questions and guessing games!
"""

import panel as pn
import pandas as pd
from typing import Dict, List, Any
import json

# Initialize Panel
pn.extension('tabulator', design='material')

# Global state to store game data
game_state = {
    'questions': [],
    'answers': {},  # {participant_name: {question_id: answer}}
    'guesses': {},  # {guesser_name: {question_id: {answer_id: guessed_name}}}
    'participants': set(),
    'phase': 'setup',  # setup, answer, game, results
    'admin_password': 'condaclaus2024'  # Simple password for admin access
}


class CondaCarolApp:
    def __init__(self):
        self.setup_view = self.create_setup_view()
        self.answer_view = self.create_answer_view()
        self.game_view = self.create_game_view()
        self.results_view = self.create_results_view()

    def create_setup_view(self):
        """Admin view to set up questions"""
        pn.state.notifications.position = 'top-right'

        title = pn.pane.Markdown("# 🎄 CondaCarol - Setup Questions 🎅")
        instructions = pn.pane.Markdown("""
        **Admin Setup**: Add questions for participants to answer.
        These should be fun, personal questions that help everyone learn about each other!
        """)

        # Password input
        password_input = pn.widgets.PasswordInput(
            name='Admin Password',
            placeholder='Enter admin password'
        )

        # Question input
        question_input = pn.widgets.TextAreaInput(
            name='Question',
            placeholder='e.g., What was your favorite vacation destination?',
            height=100
        )

        questions_list = pn.widgets.TextAreaInput(
            name='Current Questions',
            value='',
            height=300,
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
                pn.state.notifications.error('Incorrect admin password!')
                return

            if question_input.value.strip():
                game_state['questions'].append(question_input.value.strip())
                pn.state.notifications.success(f'Question added! Total: {len(game_state["questions"])}')
                question_input.value = ''
                update_questions_display()
            else:
                pn.state.notifications.warning('Please enter a question.')

        def clear_questions(event):
            if password_input.value != game_state['admin_password']:
                pn.state.notifications.error('Incorrect admin password!')
                return

            game_state['questions'] = []
            game_state['answers'] = {}
            pn.state.notifications.info('All questions cleared!')
            update_questions_display()

        def start_answer_phase(event):
            if password_input.value != game_state['admin_password']:
                pn.state.notifications.error('Incorrect admin password!')
                return

            if len(game_state['questions']) < 3:
                pn.state.notifications.error('Please add at least 3 questions!')
                return

            game_state['phase'] = 'answer'
            pn.state.notifications.success('Answer phase started! Share the link with participants.')

        add_btn = pn.widgets.Button(name='Add Question', button_type='primary')
        add_btn.on_click(add_question)

        clear_btn = pn.widgets.Button(name='Clear All Questions', button_type='danger')
        clear_btn.on_click(clear_questions)

        start_btn = pn.widgets.Button(name='Start Answer Phase →', button_type='success')
        start_btn.on_click(start_answer_phase)

        update_questions_display()

        return pn.Column(
            title,
            instructions,
            password_input,
            question_input,
            pn.Row(add_btn, clear_btn),
            questions_list,
            start_btn,
            width=800
        )

    def create_answer_view(self):
        """Participant view to answer questions"""
        title = pn.pane.Markdown("# 🎁 CondaCarol - Answer Questions 🎄")
        instructions = pn.pane.Markdown("""
        **Answer the questions below**. Your answers will be shared anonymously during the guessing game!
        """)

        name_input = pn.widgets.TextInput(
            name='Your Name',
            placeholder='Enter your name'
        )

        answer_widgets = []
        answers_column = pn.Column()

        def update_answer_form():
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
                pn.state.notifications.error('Please enter your name!')
                return

            participant_name = name_input.value.strip()

            if participant_name in game_state['answers']:
                pn.state.notifications.warning('You have already submitted answers!')
                return

            answers = {}
            for i, widget in enumerate(answer_widgets):
                if not widget.value.strip():
                    pn.state.notifications.error(f'Please answer question {i+1}!')
                    return
                answers[i] = widget.value.strip()

            game_state['answers'][participant_name] = answers
            game_state['participants'].add(participant_name)
            pn.state.notifications.success(f'Thanks {participant_name}! Your answers have been submitted.')

            # Clear form
            name_input.value = ''
            for widget in answer_widgets:
                widget.value = ''

        submit_btn = pn.widgets.Button(name='Submit Answers', button_type='primary')
        submit_btn.on_click(submit_answers)

        # Admin controls
        admin_password = pn.widgets.PasswordInput(
            name='Admin Password (to start game)',
            placeholder='Enter admin password'
        )

        participants_display = pn.widgets.TextAreaInput(
            name='Participants (Admin only)',
            value='',
            height=100,
            disabled=True
        )

        def update_participants_display():
            participants_display.value = f"Total: {len(game_state['participants'])}\n" + '\n'.join(sorted(game_state['participants']))

        def start_game_phase(event):
            if admin_password.value != game_state['admin_password']:
                pn.state.notifications.error('Incorrect admin password!')
                return

            if len(game_state['participants']) < 2:
                pn.state.notifications.error('Need at least 2 participants!')
                return

            game_state['phase'] = 'game'
            pn.state.notifications.success('Game phase started! Time to guess!')

        start_game_btn = pn.widgets.Button(name='Start Game Phase →', button_type='success')
        start_game_btn.on_click(start_game_phase)

        refresh_btn = pn.widgets.Button(name='Refresh', button_type='default')
        refresh_btn.on_click(lambda e: (update_answer_form(), update_participants_display()))

        update_answer_form()

        return pn.Column(
            title,
            instructions,
            name_input,
            answers_column,
            submit_btn,
            pn.layout.Divider(),
            pn.pane.Markdown("## Admin Controls"),
            admin_password,
            refresh_btn,
            participants_display,
            start_game_btn,
            width=800
        )

    def create_game_view(self):
        """Game view where participants guess who said what"""
        title = pn.pane.Markdown("# 🎅 CondaCarol - Guess Who! 🎄")
        instructions = pn.pane.Markdown("""
        **Read each answer and guess who wrote it!**
        Each correct guess earns you a point. Good luck!
        """)

        guesser_name_input = pn.widgets.TextInput(
            name='Your Name',
            placeholder='Enter your name to start guessing'
        )

        guesses_column = pn.Column()
        guess_widgets = {}

        def update_game_form():
            guesses_column.clear()
            guess_widgets.clear()

            if not game_state['answers']:
                guesses_column.append(pn.pane.Markdown('*No answers submitted yet...*'))
                return

            participant_list = sorted(list(game_state['participants']))

            for q_idx, question in enumerate(game_state['questions']):
                guesses_column.append(pn.pane.Markdown(f"### Question {q_idx+1}: {question}"))

                # Collect all answers for this question
                answers_for_question = []
                for participant, answers in game_state['answers'].items():
                    if q_idx in answers:
                        answers_for_question.append({
                            'participant': participant,
                            'answer': answers[q_idx]
                        })

                # Create guess widgets for each answer
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
                pn.state.notifications.error('Please enter your name!')
                return

            guesser_name = guesser_name_input.value.strip()

            # Check if all guesses are made
            for key, data in guess_widgets.items():
                if data['widget'].value == '-- Select --':
                    pn.state.notifications.error('Please make all your guesses!')
                    return

            # Store guesses
            if guesser_name not in game_state['guesses']:
                game_state['guesses'][guesser_name] = {}

            for key, data in guess_widgets.items():
                game_state['guesses'][guesser_name][key] = {
                    'guessed': data['widget'].value,
                    'correct': data['correct_answer']
                }

            pn.state.notifications.success(f'Thanks {guesser_name}! Your guesses have been submitted.')
            guesser_name_input.value = ''
            for data in guess_widgets.values():
                data['widget'].value = '-- Select --'

        submit_guess_btn = pn.widgets.Button(name='Submit Guesses', button_type='primary')
        submit_guess_btn.on_click(submit_guesses)

        # Admin controls
        admin_password = pn.widgets.PasswordInput(
            name='Admin Password (to show results)',
            placeholder='Enter admin password'
        )

        def show_results(event):
            if admin_password.value != game_state['admin_password']:
                pn.state.notifications.error('Incorrect admin password!')
                return

            if not game_state['guesses']:
                pn.state.notifications.error('No guesses submitted yet!')
                return

            game_state['phase'] = 'results'
            pn.state.notifications.success('Showing results!')

        results_btn = pn.widgets.Button(name='Show Results →', button_type='success')
        results_btn.on_click(show_results)

        refresh_btn = pn.widgets.Button(name='Refresh', button_type='default')
        refresh_btn.on_click(lambda e: update_game_form())

        update_game_form()

        return pn.Column(
            title,
            instructions,
            guesser_name_input,
            guesses_column,
            submit_guess_btn,
            pn.layout.Divider(),
            pn.pane.Markdown("## Admin Controls"),
            admin_password,
            refresh_btn,
            results_btn,
            width=800
        )

    def create_results_view(self):
        """Results view showing scores and correct answers"""
        title = pn.pane.Markdown("# 🎉 CondaCarol - Results! 🏆")

        results_column = pn.Column()

        def update_results():
            results_column.clear()

            if not game_state['guesses']:
                results_column.append(pn.pane.Markdown('*No guesses to show yet...*'))
                return

            # Calculate scores
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

            # Display leaderboard
            sorted_scores = sorted(scores.items(), key=lambda x: x[1]['correct'], reverse=True)

            leaderboard_md = "## 🏆 Leaderboard\n\n"
            for i, (name, score_data) in enumerate(sorted_scores, 1):
                medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
                leaderboard_md += f"{medal} **{name}**: {score_data['correct']}/{score_data['total']} correct ({score_data['percentage']}%)\n"

            results_column.append(pn.pane.Markdown(leaderboard_md))
            results_column.append(pn.layout.Divider())

            # Display correct answers
            results_column.append(pn.pane.Markdown("## 🎁 All Answers Revealed"))

            for q_idx, question in enumerate(game_state['questions']):
                results_column.append(pn.pane.Markdown(f"### Question {q_idx+1}: {question}"))

                for participant, answers in sorted(game_state['answers'].items()):
                    if q_idx in answers:
                        results_column.append(pn.pane.Markdown(f"- **{participant}**: *{answers[q_idx]}*"))

                results_column.append(pn.layout.Divider())

        refresh_btn = pn.widgets.Button(name='Refresh Results', button_type='default')
        refresh_btn.on_click(lambda e: update_results())

        # Admin reset
        admin_password = pn.widgets.PasswordInput(
            name='Admin Password (to reset game)',
            placeholder='Enter admin password'
        )

        def reset_game(event):
            if admin_password.value != game_state['admin_password']:
                pn.state.notifications.error('Incorrect admin password!')
                return

            game_state['questions'] = []
            game_state['answers'] = {}
            game_state['guesses'] = {}
            game_state['participants'] = set()
            game_state['phase'] = 'setup'
            pn.state.notifications.success('Game reset! Starting over.')

        reset_btn = pn.widgets.Button(name='Reset Game', button_type='danger')
        reset_btn.on_click(reset_game)

        update_results()

        return pn.Column(
            title,
            results_column,
            refresh_btn,
            pn.layout.Divider(),
            pn.pane.Markdown("## Admin Controls"),
            admin_password,
            reset_btn,
            width=800
        )

    def create_app(self):
        """Main app with phase-based navigation"""

        def get_current_view():
            phase = game_state['phase']
            if phase == 'setup':
                return self.setup_view
            elif phase == 'answer':
                return self.answer_view
            elif phase == 'game':
                return self.game_view
            elif phase == 'results':
                return self.results_view
            else:
                return pn.pane.Markdown('# Unknown phase')

        # Create a reactive view that updates based on phase
        phase_info = pn.pane.Markdown(
            f"**Current Phase**: {game_state['phase'].title()} | "
            f"**Participants**: {len(game_state['participants'])} | "
            f"**Questions**: {len(game_state['questions'])}"
        )

        def refresh_page(event):
            phase_info.object = (
                f"**Current Phase**: {game_state['phase'].title()} | "
                f"**Participants**: {len(game_state['participants'])} | "
                f"**Questions**: {len(game_state['questions'])}"
            )

        refresh_status_btn = pn.widgets.Button(name='↻ Refresh Status', button_type='default')
        refresh_status_btn.on_click(refresh_page)

        header = pn.Column(
            pn.pane.Markdown("# 🐍 CondaCarol - Christmas Party Game 🎄"),
            pn.Row(phase_info, refresh_status_btn),
            pn.layout.Divider()
        )

        # Use tabs for easy navigation
        tabs = pn.Tabs(
            ('Setup', self.setup_view),
            ('Answer Questions', self.answer_view),
            ('Play Game', self.game_view),
            ('Results', self.results_view),
            dynamic=True
        )

        return pn.Column(header, tabs, sizing_mode='stretch_width')


# Create and serve the app
app = CondaCarolApp()
template = pn.template.MaterialTemplate(
    title='CondaCarol - Christmas Party Game',
    sidebar=[
        pn.pane.Markdown("""
        ## 🎄 How to Play

        1. **Setup**: Admin adds questions
        2. **Answer**: Everyone answers
        3. **Game**: Guess who said what!
        4. **Results**: See the winners!

        ---

        **Admin Password**: `condaclaus2024`

        Made with 🐍 Panel
        """)
    ],
    main=[app.create_app()]
)

template.servable()
