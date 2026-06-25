from scratch.dsl import *

class GameManager:
    def when_flag_clicked(self):
        hide_variable("n1")
        hide_variable("n2")
        hide_variable("CorrectPos")
        hide_variable("Wrong1")
        hide_variable("Wrong2")
        hide_variable("BetulBerturut")
        hide_variable("JawapanBetul")
        hide_variable("Val1")
        hide_variable("Val2")
        hide_variable("Val3")
        hide_variable("ApplesMissed")
        
        show_variable("Markah")
        show_variable("Soalan")
        show_variable("BilanganSoalan")
        show_variable("Tahap")

        set_variable("Markah", 0)
        set_variable("BilanganSoalan", 0)
        set_variable("Tahap", 1)
        set_variable("BetulBerturut", 0)
        set_variable("Soalan", "Tekan MULA")

    def when_broadcast_StartGame(self):
        set_variable("Markah", 0)
        set_variable("BilanganSoalan", 0)
        set_variable("Tahap", 1)
        set_variable("BetulBerturut", 0)
        broadcast("NextQuestion")

    def when_broadcast_NextQuestion(self):
        if BilanganSoalan == 10:
            broadcast("GameOver")
        else:
            if Tahap == 1:
                set_variable("n1", pick_random(1, 5))
                set_variable("n2", pick_random(1, 5))
                set_variable("JawapanBetul", n1 + n2)
                set_variable("Soalan", join(n1, join(" + ", join(n2, " = ?"))))
            elif Tahap == 2:
                set_variable("n1", pick_random(1, 10))
                set_variable("n2", pick_random(1, 10))
                set_variable("JawapanBetul", n1 + n2)
                set_variable("Soalan", join(n1, join(" + ", join(n2, " = ?"))))
            else:
                set_variable("n1", pick_random(5, 10))
                # Ensure jawapan sentiasa positif (> 0)
                set_variable("n2", pick_random(1, n1 - 1))
                set_variable("JawapanBetul", n1 - n2)
                set_variable("Soalan", join(n1, join(" - ", join(n2, " = ?"))))
            
            set_variable("CorrectPos", pick_random(1, 3))
            set_variable("Wrong1", JawapanBetul + pick_random(1, 3))
            set_variable("Wrong2", JawapanBetul - pick_random(1, 2))
            if Wrong2 < 1:
                set_variable("Wrong2", JawapanBetul + 4)
            
            set_variable("ApplesMissed", 0)
            broadcast("SpawnObjects")

    def when_broadcast_AnswerCorrect(self):
        change_variable("Markah", 1)
        change_variable("BilanganSoalan", 1)
        change_variable("BetulBerturut", 1)
        if BetulBerturut == 3:
            set_variable("BetulBerturut", 0)
            if Tahap < 3:
                change_variable("Tahap", 1)
        broadcast("NextQuestion")

    def when_broadcast_AnswerWrong(self):
        broadcast("SpawnObjects")
    
    def when_broadcast_AppleHitBottom(self):
        change_variable("ApplesMissed", 1)
        if ApplesMissed == 3:
            broadcast("SpawnObjects")

class Rabbit:
    def when_flag_clicked(self):
        go_to_xy(0, -120)
        show()
    
    def when_broadcast_StartGame(self):
        go_to_xy(0, -120)
        while True:
            if key_pressed("right arrow"):
                if x_position() < 220:
                    change_x(10)
            if key_pressed("left arrow"):
                if x_position() > -220:
                    change_x(-10)

class Button2:
    def when_flag_clicked(self):
        go_to_xy(0, 0)
        show()
        say("TANGKAP JAWAPAN BETUL. Bantu watak menangkap jawapan yang betul. Klik saya untuk MULA.")
    
    def when_clicked(self):
        say("")
        hide()
        broadcast("StartGame")
    
    def when_broadcast_GameOver(self):
        go_to_xy(-100, 0)
        show()
        say(join("TAHNIAH! Permainan Tamat. Markah Anda: ", join(Markah, ". Klik saya untuk MAIN SEMULA.")))

class Button3:
    # This will be the "Keluar" button
    def when_flag_clicked(self):
        hide()
    
    def when_broadcast_GameOver(self):
        go_to_xy(100, 0)
        show()
        say("KELUAR")
    
    def when_clicked(self):
        stop("all")

class Apple1:
    def when_flag_clicked(self):
        hide()
    
    def when_broadcast_SpawnObjects(self):
        set_x(-150)
        set_y(180)
        if CorrectPos == 1:
            set_variable("Val1", JawapanBetul)
        elif CorrectPos == 2:
            set_variable("Val1", Wrong1)
        else:
            set_variable("Val1", Wrong2)
        show()
        say(Val1)
        while y_position() > -170:
            change_y(-3)
            if touching("Rabbit"):
                if Val1 == JawapanBetul:
                    play_sound("Clapping")
                    if pick_random(1, 2) == 1:
                        say("Tahniah!")
                    else:
                        say("Bagus!")
                    wait(1)
                    say("")
                    hide()
                    broadcast("AnswerCorrect")
                    set_y(-180)
                else:
                    play_sound("Oops")
                    say("Cuba Lagi!")
                    wait(2)
                    say("")
                    hide()
                    broadcast("AnswerWrong")
                    set_y(-180)
        if y_position() <= -170:
            hide()
            broadcast("AppleHitBottom")

class Apple2:
    def when_flag_clicked(self):
        hide()
    
    def when_broadcast_SpawnObjects(self):
        set_x(0)
        set_y(180)
        if CorrectPos == 2:
            set_variable("Val2", JawapanBetul)
        elif CorrectPos == 3:
            set_variable("Val2", Wrong1)
        else:
            set_variable("Val2", Wrong2)
        show()
        say(Val2)
        while y_position() > -170:
            change_y(-3)
            if touching("Rabbit"):
                if Val2 == JawapanBetul:
                    play_sound("Clapping")
                    if pick_random(1, 2) == 1:
                        say("Tahniah!")
                    else:
                        say("Bagus!")
                    wait(1)
                    say("")
                    hide()
                    broadcast("AnswerCorrect")
                    set_y(-180)
                else:
                    play_sound("Oops")
                    say("Cuba Lagi!")
                    wait(2)
                    say("")
                    hide()
                    broadcast("AnswerWrong")
                    set_y(-180)
        if y_position() <= -170:
            hide()
            broadcast("AppleHitBottom")

class Apple3:
    def when_flag_clicked(self):
        hide()
    
    def when_broadcast_SpawnObjects(self):
        set_x(150)
        set_y(180)
        if CorrectPos == 3:
            set_variable("Val3", JawapanBetul)
        elif CorrectPos == 1:
            set_variable("Val3", Wrong1)
        else:
            set_variable("Val3", Wrong2)
        show()
        say(Val3)
        while y_position() > -170:
            change_y(-3)
            if touching("Rabbit"):
                if Val3 == JawapanBetul:
                    play_sound("Clapping")
                    if pick_random(1, 2) == 1:
                        say("Tahniah!")
                    else:
                        say("Bagus!")
                    wait(1)
                    say("")
                    hide()
                    broadcast("AnswerCorrect")
                    set_y(-180)
                else:
                    play_sound("Oops")
                    say("Cuba Lagi!")
                    wait(2)
                    say("")
                    hide()
                    broadcast("AnswerWrong")
                    set_y(-180)
        if y_position() <= -170:
            hide()
            broadcast("AppleHitBottom")
