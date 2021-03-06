import random
import time

import os
from psychopy import core
from screeninfo import get_monitors
from Template_Task_Psychopy.task_template import TaskTemplate
from list_ans import L_ans, L_img


class Lucifer(TaskTemplate):
    # IMPORTANT ! To MODIFY IF NEEDED
    nb_ans = 2
    response_pad = True  # has to be set on "True" on production.
    eye_tracker_study = True  # same
    # END OF IMPORTANT
    yes_key_name = "verte"
    yes_key_code = "6"
    no_key_name = "rouge"
    no_key_code = "0"
    quit_code = "3"
    keys = ["space", yes_key_name, no_key_name, quit_code]
    launch_example = True
    trials = 100
    score = 0
    group = "common"
    exp_start_timestamp = time.time()

    next = f"Pour passer à l'instruction suivante, appuyez sur la touche {yes_key_name}"
    instructions = [
        f"Dans cette expérience : \n\n - appuyez sur la touche {yes_key_name} pour selectionner la réponse "
        f"de droite. \n\n - appuyez sur la touche {no_key_name} pour selectionner la réponse de "
        f"gauche.",
        "N'appuyez sur les touches colorées que lorsque la question apparaît.",
        f"Placez vos index sur les touches {no_key_name} et {yes_key_name}."
    ]
    csv_headers = [
        "id_candidate",
        "no_trial",
        "left_ans",
        "right_ans",
        "ans_candidate",
        "good_ans",
        "result",
        "group",
        "score",
        "reaction_time",
        "time_stamp",
    ]

    def task(self, no_trial):
        waiting_time = 2
        self.create_visual_image(image=f"img/{L_img[no_trial]}", size=[get_monitors()[0].width, get_monitors()[0].height]).draw()
        self.win.flip()
        core.wait(waiting_time)
        seed = random.randint(0, 1)
        left_ans = L_ans[no_trial][seed]
        self.create_visual_text(text=f"Combien d'allumettes avez-vous vu ? {L_ans[no_trial].pop(seed)} / {L_ans[no_trial][0]}").draw()
        self.win.flip()
        if seed:
            good_ans = self.yes_key_code
        else:
            good_ans = self.no_key_code

        time_stamp = time.time() - self.response_pad_timestamp
        resp, rt = self.get_response_with_time()

        if resp == good_ans and no_trial < 100:
            self.score += 1

        if self.response_pad:
            self.update_csv(
                self.participant,
                no_trial,
                left_ans,
                L_ans[no_trial][0],
                [left_ans if resp == self.no_key_code else L_ans[no_trial][0]][0],
                [left_ans if good_ans == self.no_key_code else L_ans[no_trial][0]][0],
                int(resp == good_ans),
                self.group,
                self.score,
                round(rt - time_stamp, 2),
                round(rt, 2),
            )
        else:
            self.update_csv(
                self.participant,
                no_trial,
                left_ans,
                L_ans[no_trial][0],
                [left_ans if resp == self.no_key_code else L_ans[no_trial][0]][0],
                [left_ans if good_ans == self.no_key_code else L_ans[no_trial][0]][0],
                int(resp == good_ans),
                self.group,
                self.score,
                round(rt, 2),
                round(time.time() - self.exp_start_timestamp, 2),
            )
        self.create_visual_text("").draw()
        self.win.flip()
        if no_trial == 49 and self.score >= 40:
            waiting_time /= 2
            self.group = "pro"

        core.wait(0.5)
        if self.launch_example:
            return resp == good_ans

    def example(self):
        score_example = 0
        example = self.create_visual_text(text="Commençons par un petit entraînement")
        tutoriel_end = self.create_visual_text(
            text="L'entraînement est désormais terminé"
        )
        example.draw()
        self.create_visual_text(self.next, pos=(0, -0.4), font_size=0.04).draw()
        self.win.flip()
        self.wait_yes(self.yes_key_code)
        for u in range(100, 103):
            if self.task(u):
                score_example += 1
                self.create_visual_text(
                    f"Bravo ! Vous avez {score_example}/{u - 99}"
                ).draw()
                self.win.flip()
                core.wait(2)
            else:
                self.create_visual_text(
                    f"Dommage... Vous avez {score_example}/{u - 99}"
                ).draw()
                self.win.flip()
                core.wait(2)
        self.create_visual_text(f"Vous avez obtenu {score_example}/3").draw()
        self.win.flip()
        core.wait(5)
        tutoriel_end.draw()
        self.win.flip()
        core.wait(5)


exp = Lucifer("csv")
exp.start()
