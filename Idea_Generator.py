import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import random

# Initializes your app with your bot token and socket mode handler
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))
# idea_type: 0=hardware 1=software 2=both 3=any/other
# idea_types = {0: "hardware ", 1: "software ",
# 2: "both hardware and software ", 3: ""}
# idea_diff: 0=easy/starter project 1=medium 2=hard 3=unsure/depends
# idea_diffs = {0: "easy", 1: "medium difficulty", 2: "hard", 3: ""}

# Listens to incoming messages that contain "hello"
# To learn available listener arguments,
"""visit https://tools.slack.dev/bolt-python/api-docs/slack_bolt/
kwargs_injection/args.html"""


class Variable_Holder:
    def __init__(self):
        self.idea_types = {0: "hardware ", 1: "software ",
                           2: "both hardware and software ", 3: ""}
        self.idea_diffs = {0: "easy ", 1: "medium difficulty ", 2: "hard ",
                           3: ""}
        self.ideas = [[[["make a pcb keychain", "U07BFSE4QFP"]], [["make a spider robot", "U07BFSE4QFP"]], [["make a pcb with only nand gates", "U07BFSE4QFP"]], [["make a computer mouse", "U07BFSE4QFP"]]],  # hardware
                      [[["make a guess my number game", "U07BFSE4QFP"]], [["make a fun game with only true and false variables", "U07BFSE4QFP"]], [["make an app that stops you from procrastinating", "U07BFSE4QFP"]], [["make a game run in the terminal", "U07BFSE4QFP"]]],  # software
                      [[["make a simple robot that moves its joints randomly", "U07BFSE4QFP"]], [["make an arcade game", "U07BFSE4QFP"]], [["design the next iphone", "U07BFSE4QFP"]], [["make a plant monitor that also takes care of it", "U07BFSE4QFP"]]],  # both
                      [[["draw a cat", "U07BFSE4QFP"]], [["design a phone case and 3D print it", "U07BFSE4QFP"]], [["join a hackathon", "U07BFSE4QFP"]], [["go to ysws.hackclub.com and do a ysws", "U07BFSE4QFP"]]]]  # other
        self.idea_type = 0
        self.idea_diff = 0
        self.wait_user_idea = False
        self.new_idea = ""
        self.anonymous = False
        self.idea_creator = "user"
        self.submission_happening = False


var_holder = Variable_Holder()


# messages
@app.message("Help")
def message_hello(message, say):
    # say() sends a message to the channel where the event was triggered
    say(text=f"(this is a WIP) Hey there <@{message['user']}>! Try running " +
        "/give_idea or /get_idea.")


@app.message("")
def handle_message(message, say, respond):
    user_id = message["user"]
    idea = message["text"]
    if var_holder.wait_user_idea:
        var_holder.wait_user_idea = False
        var_holder.new_idea = idea
        if not var_holder.anonymous:
            var_holder.idea_creator = user_id
        var_holder.ideas[var_holder.idea_type][var_holder.idea_diff].append(
            [idea, var_holder.idea_creator])
        say("Thank You!")


@app.event("message")
def handle_message_events(body, logger):
    logger.info(body)


# commands
@app.command("/give_idea")
def give_idea(ack, respond, command):
    ack()
    if not var_holder.submission_happening:
        var_holder.submission_happening = True
        respond(
            blocks=[
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"Hi <@{command['user_id']}>! " +
                        "What type of idea would you like to give?"
                    }
                },
                {
                    "type": "actions",
                    "elements": [
                        {
                            "type": "button",
                            "text": {"type": "plain_text", "text": "Hardware"},
                            "action_id": "give_hardware",
                            "value": "hardware"
                        },
                        {
                            "type": "button",
                            "text": {"type": "plain_text", "text": "Software"},
                            "action_id": "give_software",
                            "value": "software"
                        },
                        {
                            "type": "button",
                            "text": {"type": "plain_text", "text":
                                     "Both Hardware and Software"},
                            "action_id": "give_both",
                            "value": "both"
                        },
                        {
                            "type": "button",
                            "text": {"type": "plain_text", "text": "Other"},
                            "action_id": "give_other",
                            "value": "other"
                        }
                    ]
                }
            ],
            text="What type of idea would you like to give?"
        )
    else:
        respond("Someone else is currently submitting an idea. Please wait a" +
                " moment and try again.")


@app.command("/get_idea")
def get_idea(ack, respond, command):
    # Acknowledge command request
    ack()
    if not var_holder.submission_happening:
        var_holder.submission_happening = True
        respond(
            blocks=[
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"Hi <@{command['user_id']}>! " +
                        "What type of idea do you need?"
                    }
                },
                {
                    "type": "actions",
                    "elements": [
                        {
                            "type": "button",
                            "text": {"type": "plain_text", "text": "Hardware"},
                            "action_id": "get_hardware",
                            "value": "hardware"
                        },
                        {
                            "type": "button",
                            "text": {"type": "plain_text", "text": "Software"},
                            "action_id": "get_software",
                            "value": "software"
                        },
                        {
                            "type": "button",
                            "text": {"type": "plain_text", "text":
                                     "Both Hardware and Software"},
                            "action_id": "get_both",
                            "value": "both"
                        },
                        {
                            "type": "button",
                            "text": {"type": "plain_text", "text": "Any"},
                            "action_id": "get_any",
                            "value": "any"
                        }
                    ]
                }
            ],
            text="What type of idea do you need?"
            # Fallback text for accessibility
        )
    else:
        respond("Someone else is currently requesting an idea. Please wait a" +
                " moment and try again.")


# ask for idea difficulty
def ask_idea_diff_give(respond):
    respond(
        blocks=[
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "What difficulty is your " +
                    f"{var_holder.idea_types[var_holder.idea_type]}idea?"}
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {"type": "plain_text", "text": "Easy"},
                        "action_id": "give_easy",
                        "value": "easy"
                    },
                    {
                        "type": "button",
                        "text": {"type": "plain_text", "text": "Medium"},
                        "action_id": "give_medium",
                        "value": "medium"
                    },
                    {
                        "type": "button",
                        "text": {"type": "plain_text", "text": "Hard"},
                        "action_id": "give_hard",
                        "value": "hard"
                    },
                    {
                        "type": "button",
                        "text": {"type": "plain_text", "text":
                                 "Don't know/Varies"},
                        "action_id": "give_other_diff",
                        "value": "other"
                    }
                ]
            }
        ],
        text="What difficulty is your idea?")


def ask_idea_diff_get(respond):
    respond(
        blocks=[
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "What difficulty do you want your " +
                    f"{var_holder.idea_types[var_holder.idea_type]}" +
                    "idea to be?"}
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {"type": "plain_text", "text": "Easy"},
                        "action_id": "get_easy",
                        "value": "easy"
                    },
                    {
                        "type": "button",
                        "text": {"type": "plain_text", "text": "Medium"},
                        "action_id": "get_medium",
                        "value": "medium"
                    },
                    {
                        "type": "button",
                        "text": {"type": "plain_text", "text": "Hard"},
                        "action_id": "get_hard",
                        "value": "hard"
                    },
                    {
                        "type": "button",
                        "text": {"type": "plain_text", "text":
                                 "Any"},
                        "action_id": "get_any_diff",
                        "value": "any"
                    }
                ]
            }
        ],
        text="What difficulty do you want your idea to be?")


# button actions

# step 1 give
@app.action("give_hardware")
def hardware_given(ack, respond, action, say):
    ack()
    var_holder.idea_type = 0
    ask_idea_diff_give(respond)


@app.action("give_software")
def software_given(ack, respond, action, say):
    ack()
    var_holder.idea_type = 1
    ask_idea_diff_give(respond)


@app.action("give_both")
def both_given(ack, respond, action, say):
    ack()
    var_holder.idea_type = 2
    ask_idea_diff_give(respond)


@app.action("give_other")
def other_given(ack, respond, action, say):
    ack()
    var_holder.idea_type = 3
    ask_idea_diff_give(respond)


# step 1 get
@app.action("get_hardware")
def hardware_gotten(ack, respond, action, say):
    ack()
    var_holder.idea_type = 0
    ask_idea_diff_get(respond)


@app.action("get_software")
def software_gotten(ack, respond, action, say):
    ack()
    var_holder.idea_type = 1
    ask_idea_diff_get(respond)


@app.action("get_both")
def both_gotten(ack, respond, action, say):
    ack()
    var_holder.idea_type = 2
    ask_idea_diff_get(respond)


@app.action("get_any")
def any_gotten(ack, respond, action, say):
    ack()
    var_holder.idea_type = 3
    ask_idea_diff_get(respond)


# step 2

# step 2 get
@app.action("get_easy")
def easy_gotten(ack, respond, action, say):
    ack()
    var_holder.idea_diff = 0
    fetch_idea(say, ack, respond)


@app.action("get_medium")
def medium_gotten(ack, respond, action, say,
                  idea_diffs):
    ack()
    var_holder.idea_diff = 1
    fetch_idea(say, ack, respond)


@app.action("get_hard")
def hard_gotten(ack, respond, action, say):
    ack()
    var_holder.idea_diff = 2
    fetch_idea(say, ack, respond)


@app.action("get_any_diff")
def any_diff_gotten(ack, respond, action, say):
    ack()
    var_holder.idea_diff = 3
    fetch_idea(say, ack, respond)


# finish get
def fetch_idea(say, ack, respond):
    ack()
    respond(f"fetching your {var_holder.idea_diffs[var_holder.idea_diff]}" +
            f"{var_holder.idea_types[var_holder.idea_type]}idea...")
    if var_holder.idea_type == 3:
        var_holder.idea_type = random.randint(0, 2)
    if var_holder.idea_diff == 3:
        var_holder.idea_diff = random.randint(0, 2)
    random_idea = random.choice(
        var_holder.ideas[var_holder.idea_type][var_holder.idea_diff])
    say("You should: " + random_idea[0])
    if random_idea[1] != "anonymous":
        say(f"Thanks to <@{random_idea[1]}> for this idea!")


# step 2 give
@app.action("give_easy")
def give_easy(ack, respond, action):
    ack()
    var_holder.idea_diff = 0
    ask_idea(respond)


@app.action("give_medium")
def give_medium(ack, respond, action):
    ack()
    var_holder.idea_diff = 1
    ask_idea(respond)


@app.action("give_hard")
def give_hard(ack, respond, action):
    ack()
    var_holder.idea_diff = 2
    ask_idea(respond)


@app.action("give_other_diff")
def give_other_diff(ack, respond, action):
    ack()
    var_holder.idea_diff = 3
    ask_idea(respond)


# step 3 give
def ask_idea(respond):
    respond(
        blocks=[
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "Do you want your username attached to your idea?"
                }
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {"type": "plain_text", "text": "Yes"},
                        "action_id": "username",
                        "value": "yes"
                    },
                    {
                        "type": "button",
                        "text": {"type": "plain_text", "text": "No"},
                        "action_id": "anonymous",
                        "value": "no"
                    }
                ]
            }
        ],
        text="Do you want your username attached to your idea?"
        # Fallback text for accessibility
    )


@app.action("username")
def collect_username(ack, respond):
    ack()
    var_holder.anonymous = False
    last_step(respond)


@app.action("anonymous")
def dont_collect_username(ack, respond):
    ack()
    var_holder.anonymous = True
    last_step(respond)


def last_step(respond):
    respond("One last step: please send your idea. Example: make a slack bot" +
            " that gives and recieves ideas")
    var_holder.wait_user_idea = True


# Start the app
if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
