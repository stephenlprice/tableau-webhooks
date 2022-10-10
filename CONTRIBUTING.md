# CONTRIBUTING

This repository is managed by way of the [project kanban](https://github.com/stephenlprice/tableau-webhooks/projects/1). It organizes issues into "To do", "In progress" and "Done" columns similar to a Trello board.

A great way to contribute to this project is to find an open issue under the "To do" column, assigning it to yourself and moving it to "In progress". 

The kanban is automated, meaning that if you have an open issue that is ready to be merged into the `main` branch, you should create a pull request and associate the issue number with a closing statement in the pull request's description such as `Closes #12`. That way when the pull request is reviewed and later approved, the merge itself will automatically close the issue and move it to the "Done" column in the project kanban.

All enhancements and bug fixes to the code base are performed by way of a pull request to the `main` branch following a review and approval of the proposed commits.

## Enhancements, bugs and other issues

To request new features, to describe bugs, to document something new or to ask for help with a problem encountered while using this project you can create a new issue. Please provide as clear as a description as possible.

Make use of issue labels to help maintainers organize requests appropriately, for example new features should have the "enhancement" lagel, bugs should be labelled as "bug".

## Review process

In order to merge code into the `main` branch, a pull request must be created so that proposed commits can be properly reviewed and approved. Any new commits to the pull request branch will automatically cause existing approvals to go stale and will require a new review.

## Development

Please refer to the instructions provided in the [README.md](README.md) file. It contains instructions for requirements, environment variables, local developement and deployment.
