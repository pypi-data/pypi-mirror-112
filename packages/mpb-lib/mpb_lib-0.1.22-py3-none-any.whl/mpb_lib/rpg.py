from random import random
from time import sleep

from IPython.display import display, HTML
try:
    from google.colab.output import eval_js
except:
    def eval_js(js):
        body = HTML(f"""<script>
        {js}
        </script>""")
        display(body)

HTML_FRAME = HTML("""
 <link href="https://fonts.googleapis.com/css?family=M+PLUS+Rounded+1c&amp;subset=japanese" rel="stylesheet">
 <link rel="stylesheet" href="https://fonts.googleapis.com/icon?family=Material+Icons">
 <style>

#box {
    font-family: 'M PLUS Rounded 1c', sans-serif;
    font-size: 14pt;
    color : #ffffff;
    text-shadow : 2px 2px 2px rgba(51, 51, 51, 0.8);
    background-color : #0033cc;
    background : linear-gradient(#3366ff, #0033cc, #000066);
    padding : 12px 16px;
    box-shadow :
        3px 3px 5px rgba(51, 51, 51, 0.7) inset,
        0 0 2px 3px #666666,
        0 0 0   6px #ffffff,
        0 0 2px 8px #666666;
    width: 90%;
    margin: auto;
    margin-top: 8px;
    margin-bottom: 8px;
}

#box dt {
    font-weight: bold;
    color: #e84;
    margin: 0.4em 0 0 0;
    font-size: 16pt;
}

#box dd {
    font-weight: bold;
    padding: 0.1em 0;
}

.button {
    font-size: 12pt;
}


</style>
<div>
  <div id='box'>
  </div>
</div>
<script>
function add_message(m, e) {
    var elem = document.getElementById('box');
    var child = document.createElement(e);
    child.innerHTML     = m;
    elem.appendChild(child)
}

function add_rawhtml(h) {
    var elem = document.getElementById('box');
    elem.innerHTML += h;
}

</script>
""")

INITIAL_OUTPUT = """
<script src="https://cdnjs.cloudflare.com/ajax/libs/howler/2.2.3/howler.min.js"></script>
<script>
var death = new Howl({
    src: ['https://github.com/shibats/mpb_samples/blob/main/assets/deth.mp3?raw=true'],
    preload: true,
    html5: true
});

var hero_emerge = new Howl({
    src: ['https://github.com/shibats/mpb_samples/blob/main/assets/hero_emerge.mp3?raw=true'],
    preload: true,
    html5: true
});

var hit1 = new Howl({
    src: ['https://github.com/shibats/mpb_samples/blob/main/assets/hit1.mp3?raw=true'],
    preload: true,
    html5: true
});

var hit2 = new Howl({
    src: ['https://github.com/shibats/mpb_samples/blob/main/assets/hit2.mp3?raw=true'],
    preload: true,
    html5: true
});

var monster_emerge = new Howl({
    src: ['https://github.com/shibats/mpb_samples/blob/main/assets/monster_emerge.mp3?raw=true'],
    preload: true,
    html5: true
});

var success = new Howl({
    src: ['https://github.com/shibats/mpb_samples/blob/main/assets/success.mp3?raw=true'],
    preload: true,
    html5: true
});

var status = new Howl({
    src: ['https://github.com/shibats/mpb_samples/blob/main/assets/status.mp3?raw=true'],
    preload: true,
    html5: true
});

var fight_music = new Howl({
    src: ['https://github.com/shibats/mpb_samples/blob/main/assets/fight_music.mp3?raw=true'],
    preload: true,
    html5: true
});
/*Howler.autoUnlock = true;*/

</script>

"""
# preload mp3s.

def load_audio():
    body = HTML(INITIAL_OUTPUT)
    display(body)


def play_audio(the_id):
    display(HTML(f"""<script>
    {the_id}.play();
    </script>
    """))


def pause_audio(the_id):
    display(HTML(f"""<script>
        {the_id}.stop();
        </script>
    """))


load_audio()

def play_with_button(sound_id, PLAYABLE):
    if PLAYABLE:
        play_audio(sound_id)
    else:
        rawhtml = f"""add_rawhtml('<button class="button" onclick="javascript:{sound_id}.play();"><span class="material-icons">volume_up</span>音を出す</button>"""
        rawhtml += f"""<button class="button" onclick="javascript:{sound_id}.stop();"><span class="material-icons">volume_off</span>音を消す</button>')"""
        eval_js(rawhtml)



def add_message(message, elem="p"):
    """
    JavaScriptをinvokeして出力にメッセージを追加するユーティリティ関数
    """
    eval_js(f"add_message('{message}', '{elem}')")



class ユニット:
    PLAYABLE = False


    def __init__(self, kind):
        try:
            display(HTML(f"""
        <audio id="nosound" preload>
        <source src="https://github.com/shibats/mpb_samples/blob/main/assets/nosound.mp3?raw=true" type="audio/mp3">
        </audio>
            """))
            eval_js(f"""
                    var bgm1 = document.querySelector("#nosound");
                    bgm1.play();
                    """)
        except:
            self.__class__.PLAYABLE = False


        self.kind = kind
        self.体力 = 0
        self.パワー = 0
        load_audio()

        sound_id = "monster_emerge"
        if kind == "戦士":
            sound_id = "hero_emerge"

        display(HTML_FRAME)
        play_with_button(sound_id, self.PLAYABLE)
        add_message(f"{self.kind}がうまれた。")


    def ステータス(self):

        load_audio()

        display(HTML_FRAME)

        play_with_button("status", self.PLAYABLE)

        add_message(f"ステータス", "dt")
        add_message(f"職業　 : {self.kind: >5}", "dd")
        add_message(f"体力　 : {self.体力: >5}", "dd")
        add_message(f"パワー : {self.パワー: >5}", "dd")


    def 戦う(self, target):
        load_audio()
        display(HTML_FRAME)

        if self.体力 <= 0:
            add_message(f"{self.kind}は死んでいるので戦えない。")
            play_with_button("death", self.PLAYABLE)
            return

        if target.体力 <= 0:
            add_message(f"{target.kind}は死んでいる。これ以上はかわいそうだ。")
            play_with_button("death", self.PLAYABLE)
            return

        damage_mine = int(target.パワー*(random()/2+0.5))
        damage_targets = int(self.パワー*(random()/2+0.5))
        self.体力 -= damage_mine
        target.体力 -= damage_targets

        play_with_button("fight_music", self.PLAYABLE)

        add_message(f"{self.kind}と{target.kind}が戦った。")
        sleep(2)
        play_audio("hit1")
        add_message(f"{self.kind}が{target.kind}に{damage_targets}のダメージを与えた。")
        sleep(1)

        if target.体力 <= 0:
            pause_audio("fight_music")
            play_audio("success")
            add_message(f"{self.kind}は{target.kind}を倒した！")
            return

        add_message(f"{target.kind}が{self.kind}に{damage_mine}のダメージを与えた。")
        play_audio("hit1")
        sleep(1)

        if self.体力 <= 0:
            pause_audio("fight_music")
            play_audio("death")
            add_message(f"{self.kind}は{target.kind}に倒されて死んでしまった。")


class Unit:

    def __init__(self, kind):
        self.kind = kind
        self.hitpoint = 0
        self.strength = 0
        print(f"{self.kind} was born.")


    def status(self):
        print("-"*20)
        print(f"Occupation : {self.kind: >5}")
        print(f"Hitpoint   : {self.hitpoint: >5}")
        print(f"Strength   : {self.strength: >5}")
        print("-"*20)


    def fight(self, target):
        if self.hitpoint <= 0:
            print(f"{self.kind} has been already dead.")
            return

        if target.hitpoint <= 0:
            print(f"{target.kind} had died.")
            return

        damage_mine = int(target.strength*(random()/2+0.5))
        damage_targets = int(self.strength*(random()/2+0.5))
        self.hitpoint -= damage_mine
        target.hitpoint -= damage_targets
        print(f"{self.kind} fought with {target.kind}.")
        print(f"{self.kind} gave {damage_targets} damage to {target.kind}.")

        if target.strength <= 0:
            print(f"{self.kind} beat {target.kind} !")
            return

        print(f"{target.kind} gave {damage_mine} damage to {self.kind}.")

        if self.hitpoint <= 0:
            print(f"{self.kind} has been defeated by {target.kind}.")
