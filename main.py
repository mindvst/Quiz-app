from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button


class QuizApp(App):

    def build(self):
        self.questions = [
            ("What is the capital of India?",
             ["Mumbai", "Delhi", "Kolkata", "Chennai"], "Delhi"),

            ("How many days are in a week?",
             ["5", "6", "7", "8"], "7"),

            ("Which planet is called the Red Planet?",
             ["Earth", "Mars", "Jupiter", "Venus"], "Mars"),

            ("What is 10 + 5?",
             ["10", "15", "20", "25"], "15"),

            ("Which animal is known as the King of the Jungle?",
             ["Tiger", "Lion", "Bear", "Elephant"], "Lion")
        ]

        self.layout = BoxLayout(
            orientation="vertical",
            padding=30,
            spacing=15
        )

        self.timer = Label(
            text="Time: 10",
            font_size=22
        )

        self.question = Label(
            text="",
            font_size=24
        )

        self.result = Label(
            text="",
            font_size=20
        )

        self.layout.add_widget(self.timer)
        self.layout.add_widget(self.question)

        self.buttons = []

        for i in range(4):
            button = Button(
                text="",
                font_size=20
            )
            button.bind(on_press=self.check_answer)
            self.buttons.append(button)
            self.layout.add_widget(button)

        self.next_button = Button(
            text="NEXT",
            font_size=20
        )
        self.next_button.bind(on_press=self.next_question)

        self.restart_button = Button(
            text="RESTART QUIZ",
            font_size=20
        )
        self.restart_button.bind(on_press=self.restart_quiz)
        self.restart_button.disabled = True

        self.layout.add_widget(self.next_button)
        self.layout.add_widget(self.restart_button)
        self.layout.add_widget(self.result)

        self.restart_quiz(None)

        return self.layout

    def show_question(self):

        self.time_left = 10

        q, options, answer = self.questions[self.current]

        self.question.text = (
            "Question " + str(self.current + 1)
            + "\n\n" + q
        )

        for i in range(4):
            self.buttons[i].text = options[i]
            self.buttons[i].disabled = False

        self.result.text = "Score: " + str(self.score)
        self.next_button.disabled = True
        self.restart_button.disabled = True

        Clock.unschedule(self.update_timer)
        Clock.schedule_interval(self.update_timer, 1)

    def update_timer(self, dt):

        self.time_left -= 1
        self.timer.text = "Time: " + str(self.time_left)

        if self.time_left <= 0:

            Clock.unschedule(self.update_timer)

            self.result.text = "Time Up!"

            for button in self.buttons:
                button.disabled = True

            self.next_button.disabled = False

    def check_answer(self, button):

        Clock.unschedule(self.update_timer)

        correct_answer = self.questions[self.current][2]

        if button.text == correct_answer:
            self.score += 1
            self.result.text = "Correct!"
        else:
            self.result.text = "Wrong! Correct: " + correct_answer

        for button in self.buttons:
            button.disabled = True

        self.next_button.disabled = False

    def next_question(self, button):

        self.current += 1

        if self.current < len(self.questions):
            self.show_question()
        else:
            self.finish_quiz()

    def finish_quiz(self):

        Clock.unschedule(self.update_timer)

        self.question.text = (
            "QUIZ COMPLETE!\n\n"
            "Your Score: "
            + str(self.score)
            + "/"
            + str(len(self.questions))
        )

        self.timer.text = ""
        self.result.text = "Thanks for playing!"

        for button in self.buttons:
            button.text = ""
            button.disabled = True

        self.next_button.disabled = True
        self.restart_button.disabled = False

    def restart_quiz(self, button):

        Clock.unschedule(self.update_timer)

        self.score = 0
        self.current = 0

        self.next_button.disabled = True
        self.restart_button.disabled = True

        self.show_question()


QuizApp().run()