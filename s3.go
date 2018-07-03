package main

import (
	"os"

	"encoding/json"
	"fmt"
	"github.com/aws/aws-sdk-go/aws"
	"github.com/aws/aws-sdk-go/aws/session"
	"github.com/aws/aws-sdk-go/service/s3"
	"github.com/aws/aws-sdk-go/service/s3/s3manager"
	"io/ioutil"
)

const myBucket = "octopombo"

type Project struct {
	Name           string `json:"name"`
	ApprovalsCount int    `json:"approvals_count"`
}

type Repositories struct {
	Name string
}

func (p Project) toString() string {
	return toJson(p)
}

func toJson(p interface{}) string {
	bytes, err := json.Marshal(p)
	if err != nil {
		fmt.Println(err.Error())
		os.Exit(1)
	}

	return string(bytes)
}

func convertToBytes(p []Project) []byte {
	bytes, err := json.Marshal(p)
	if err != nil {
		fmt.Println(err.Error())
		os.Exit(1)
	}

	return bytes
}

func convertToProject(raw []byte) []Project {
	var projects []Project
	json.Unmarshal(raw, &projects)
	return projects
}

func DownloadManager(filename string) ([]byte, error) {
	sess := session.Must(session.NewSession(&aws.Config{
		Region: aws.String("us-east-1")},
	))

	downloader := s3manager.NewDownloader(sess)

	f, err := os.Create(filename)
	if err != nil {
		fmt.Println("failed to create file %q, %v", filename, err)
		return nil, err
	}

	_, err = downloader.Download(f, &s3.GetObjectInput{
		Bucket: aws.String(myBucket),
		Key:    aws.String(filename),
	})

	if err != nil {
		fmt.Println("failed to download file, %v", err)
		return []byte{}, nil
	}

	raw, err := ioutil.ReadFile(fmt.Sprintf("./%s", filename))
	if err != nil {
		fmt.Println(err.Error())
		return nil, err
	}

	return raw, nil

}

func UploadManager(filename string) error {
	sess := session.Must(session.NewSession(&aws.Config{
		Region: aws.String("us-east-1")},
	))

	// Create an uploader with the session and default options
	uploader := s3manager.NewUploader(sess)
	file, err := os.Open(filename)
	if err != nil {
		fmt.Println("Failed to open file", file, err)
	}
	defer file.Close()

	// Upload the file to S3.
	result, err := uploader.Upload(&s3manager.UploadInput{
		Bucket: aws.String(myBucket),
		Key:    aws.String(filename),
		Body:   file,
	})
	if err != nil {
		return fmt.Errorf("failed to upload file, %v", err)
	}
	fmt.Printf("file uploaded to, %s\n", aws.StringValue(&result.Location))
	return nil
}

func GetApprovalsCount(ch string, repo string) int {
	filename := fmt.Sprintf("%s.json", ch)

	raw, err := DownloadManager(filename)
	if err != nil {
		fmt.Println("An error occurred downloading file, error: ", err)
	}
	projects := convertToProject(raw)

	for _, project := range projects {
		if project.Name == repo {
			return project.ApprovalsCount
		}
	}
	return 2
}

func GetRepositories(ch string) []*Repositories {
	filename := fmt.Sprintf("%s.json", ch)

	raw, err := DownloadManager(filename)
	if err != nil {
		fmt.Println("An error occurred downloading file, error: ", err)
	}
	projects := convertToProject(raw)

	var myRepos []*Repositories

	for _, project := range projects {
		repo := &Repositories{Name: project.Name}
		myRepos = append(myRepos, repo)
	}
	return myRepos
}

func AddRepo(ch string, repo string, approvals int) (bool, error) {
	filename := fmt.Sprintf("%s.json", ch)
	projects := []Project{}
	project := Project{Name: repo, ApprovalsCount: approvals}

	raw, err := DownloadManager(filename)
	if err != nil {
		fmt.Println("An error occurred downloading file, error: ", err)
	}

	projects = convertToProject(raw)
	for _, project := range projects {
		if project.Name == repo {
			return false, nil
		}
	}
	projects = append(projects, project)
	projectByte := convertToBytes(projects)

	f, err := os.Create(filename)
	if err != nil {
		fmt.Println("An Error occurred creating file", err)
	}

	_, err = f.Write(projectByte)
	if err != nil {
		fmt.Println("An Error occurred writing in a file", err)
	}

	defer f.Close()

	err = UploadManager(filename)
	if err != nil {
		fmt.Println("Error uploading file, error: ", err)
		return false, err
	}

	return true, nil
}

func RemoveRepo(ch string, repo string) (bool, error) {
	filename := fmt.Sprintf("%s.json", ch)
	removed := false
	raw, err := DownloadManager(filename)
	if err != nil {
		fmt.Println("An error occurred downloading file, error: ", err)
	}

	projects := convertToProject(raw)
	for index, project := range projects {
		if project.Name == repo {
			projects = append(projects[:index], projects[index+1:]...)
			removed = true
		}
	}

	projectByte := convertToBytes(projects)

	f, err := os.Create(filename)
	if err != nil {
		fmt.Println("An Error occurred creating file", err)
	}

	_, err = f.Write(projectByte)
	if err != nil {
		fmt.Println("An Error occurred writing in a file", err)
	}

	defer f.Close()

	err = UploadManager(filename)
	if err != nil {
		fmt.Println("Error uploading file, error: ", err)
		return false, err
	}

	return removed, nil
}
