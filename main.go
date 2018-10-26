package main

import (
	"fmt"
	"github.com/nlopes/slack"
	"os"
	"strconv"
	"strings"
)

func main() {

	token := os.Getenv("SLACK_TOKEN")
	api := slack.New(token)
	api.SetDebug(true)

	rtm := api.NewRTM()
	go rtm.ManageConnection()

Loop:
	for {
		select {
		case msg := <-rtm.IncomingEvents:
			fmt.Print("Event Received: ")
			switch ev := msg.Data.(type) {
			case *slack.ConnectedEvent:
				fmt.Println("Connection counter:", ev.ConnectionCount)

			case *slack.MessageEvent:
				fmt.Printf("Message: %v\n", ev)
				info := rtm.GetInfo()
				prefix := fmt.Sprintf("<@%s> ", info.User.ID)

				if ev.User != info.User.ID && strings.HasPrefix(ev.Text, prefix) {
					respond(rtm, ev, prefix)
				}

			case *slack.RTMError:
				fmt.Printf("Error: %s\n", ev.Error())

			case *slack.InvalidAuthEvent:
				fmt.Printf("Invalid credentials")
				break Loop

			default:
				//Take no action
			}
		}
	}
}

func respond(rtm *slack.RTM, msg *slack.MessageEvent, prefix string) {
	var response string
	groupInfo, err := rtm.GetGroupInfo(msg.Channel)
	if err != nil {
		fmt.Println("Error getting group Info, error: %s", err)
	}

	channelName := groupInfo.NameNormalized
	args := strings.SplitN(msg.Text, " ", 3)
	text := args[1]
	text = strings.TrimPrefix(text, prefix)
	text = strings.TrimSpace(text)
	text = strings.ToLower(text)

	acceptedPrs := map[string]bool{
		"show-prs": true,
		"show-pr":  true,
		"show":     true,
		"prs":      true,
	}

	acceptedAddrepos := map[string]bool{
		"add-repos": true,
		"add":       true,
		"add-repo":  true,
	}

	acceptedRemoveRepos := map[string]bool{
		"remove":      true,
		"remove-repo": true,
		"delete":      true,
	}

	if acceptedPrs[text] {
		response = "Pruuuu buscando, aguarde um minuto..."
		rtm.SendMessage(rtm.NewOutgoingMessage(response, msg.Channel))
		response = ShowPullRequests(channelName)

	} else if acceptedAddrepos[text] {
		args = strings.Split(args[2], " ")
		if !(len(args) == 2) {
			response = "Pruuu errou os argumentos"
		} else {
			repo := args[0]
			approvals, _ := strconv.Atoi(args[1])
			response = AddRepository(channelName, repo, approvals)
		}

	} else if acceptedRemoveRepos[text] {
		response = RemoveRepository(channelName, args[2])

	} else {
		response = "Pruu errou o comando. Comandos suportados no momento:```show-prs (optional) resume\nadd-repo name-of-repo number-of-approvals\nremove-repo name-of-repo\nhelp```"
	}
	rtm.SendMessage(rtm.NewOutgoingMessage(response, msg.Channel))
}
