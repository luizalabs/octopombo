package main

import (
	"context"
	"fmt"
	"github.com/google/go-github/github"
	"golang.org/x/oauth2"
	"os"
)

type PullRequests struct {
	Title          string
	URL            string
	RepositoryName string
	Approved       bool
}

var (
	owner        = os.Getenv("OWNER")
	ignoreLabels = map[string]bool{
		"approved": true,
		"blocked":  true,
	}
	channelName = ""
)

func GithubClient(ch string) (string, error) {
	ctx := context.Background()
	channelName = ch
	token := os.Getenv("GITHUB_TOKEN")
	ts := oauth2.StaticTokenSource(
		&oauth2.Token{AccessToken: token},
	)
	tc := oauth2.NewClient(ctx, ts)

	client := github.NewClient(tc)
	myRepos := GetRepositories(ch)
	prs, err := GetPullRequests(ctx, client, myRepos)
	if err != nil {
		fmt.Println("An error occurred getting Pull Requests: ", err)
		return "", nil
	}

	stringPrs := ToString(prs)
	return stringPrs, nil
}

func GetPullRequests(ctx context.Context, client *github.Client, myRepos []*Repositories) ([]*PullRequests, error) {

	opt := &github.IssueListByRepoOptions{State: "open"}
	var pulls []*PullRequests

	for _, repo := range myRepos {
		issues, _, err := client.Issues.ListByRepo(ctx, owner, repo.Name, opt)
		if err != nil {
			return pulls, err
		}
		for _, issue := range issues {
			if issue.IsPullRequest() {
				if !(IsApproved(ctx, client, repo.Name, issue)) {
					pull := &PullRequests{
						Title:          *issue.Title,
						URL:            *issue.HTMLURL,
						RepositoryName: repo.Name,
					}
					pulls = append(pulls, pull)
				}
			}
		}
	}
	for _, pull := range pulls {
		fmt.Println("PULL: ", pull)
	}
	return pulls, nil
}

func IsApproved(ctx context.Context, client *github.Client, repo string, issue *github.Issue) bool {
	var hasLabel = false

	if issue.Number != nil {
		isApprovedIssue, err := hasApprovals(ctx, client, repo, *issue.Number)
		if err != nil {
			fmt.Println("Error getting reviews, error:", err)
		}
		if isApprovedIssue {
			return true
		}
	}

	for _, labels := range issue.Labels {
		if ignoreLabels[*labels.Name] {
			hasLabel = true
			break
		}
	}

	return hasLabel
}

func hasApprovals(ctx context.Context, client *github.Client, repo string, issueID int) (bool, error) {
	approvalsCount := GetApprovalsCount("test-bot-nicolas", repo)
	reviews, _, err := client.PullRequests.ListReviews(ctx, owner, repo, issueID, nil)
	requestChanges := []string{}
	approved := []string{}
	if err != nil {
		return false, err
	}
	for _, review := range reviews {
		if *review.State == "CHANGES_REQUESTED" {
			if StringInSlice(*review.User.Login, requestChanges) == -1 {
				requestChanges = append(requestChanges, *review.User.Login)
			}
			approvedIndex := StringInSlice(*review.User.Login, approved)
			if approvedIndex >= 0 {
				approved = append(approved[:approvedIndex], approved[approvedIndex+1:]...)
			}
		} else if *review.State == "APPROVED" {
			if StringInSlice(*review.User.Login, approved) == -1 {
				approved = append(approved, *review.User.Login)
			}
			requestChangesIndex := StringInSlice(*review.User.Login, requestChanges)
			if requestChangesIndex >= 0 {
				requestChanges = append(requestChanges[:requestChangesIndex], requestChanges[requestChangesIndex+1:]...)
			}
		}
	}
	if len(approved) >= approvalsCount && len(requestChanges) == 0 {
		return true, nil
	}

	return false, nil
}

func ToString(prs []*PullRequests) string {
	response := ""
	for _, pr := range prs {
		response += fmt.Sprintf("%s - %s\n", pr.URL, pr.Title)
	}

	return response
}
