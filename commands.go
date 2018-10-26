package main

import (
	"fmt"
)

func AddRepository(channelName string, repo string, approvals int) string {
	add, err := AddRepo(channelName, repo, approvals)
	if err != nil {
		fmt.Printf("An error occurred adding file on s3, error: %s", err)
	}
	if add {
		return "Pruu pruu Repositório adicionado com sucesso."
	}
	return "Pruu esse repositório já foi adicionado antes."
}

func RemoveRepository(channelName string, repo string) string {
	removed, err := RemoveRepo(channelName, repo)
	if err != nil {
		fmt.Printf("An error occurred removing file on s3, error: %s", err)
	}
	if removed {
		return "Pruu pruu Repositório removido com sucesso."
	}
	return "Pruu esse repositório não está sendo monitorado."
}

func ShowPullRequests(channelName string) string {
	response, err := GithubClient(channelName)
	if err != nil {
		fmt.Println("Error getting pull requests, error: ", err)
		return "Ocorreu um erro ao buscar os pull requests :disappointed:"
	}
	if len(response) == 0 {
		response = "Não há PR's para serem revisados! "
	}
	return response
}
