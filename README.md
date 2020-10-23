# GitHub Required Labels
[![Build Status](https://travis-ci.com/dimagi/required-labels.svg?branch=master)](https://travis-ci.com/dimagi/required-labels)

:label: Automated label checking for GitHub pull requests.

![Label requirements satisfied](https://user-images.githubusercontent.com/146896/34694324-a926ebfe-f494-11e7-983f-b10e10719c83.png)
![Label requirements not satisfied](https://user-images.githubusercontent.com/146896/34694323-a90da090-f494-11e7-8f44-ae6780390fc9.png)

**required-labels** enforces label rules on your pull requests. We use this at [Dimagi](https://www.dimagi.com) to alert our product and design teams of external-facing changes we are making to our code.

Check it out in action [here](https://github.com/dimagi/required-labels/pulls?q=is%3Aopen+is%3Apr+label%3Aexamples).

There is also a longer write-up on this project [here](https://www.dimagi.com/blog/designing-a-foolproof-system-for-communicating-changes-made-to-your-software-product/).

You can set customized label requirements for your PRs to enforce particular team workflows with lists of "required", "banned" or "at least one" labels. For example:

- Your team requires all PRs to get sign-off from your Architecture and UX teams before being merged
    - Set **`REQUIRED_LABELS_ALL`** to `ux-signoff, arch-signoff`. This will ensure that the `ux-signoff` and `arch-sigoff` labels have been added to that PR before allowing it to be merged.
- Your team uses a certain label to flag something as "work in progress" that should never be merged until the label is removed.
    - Set **`BANNED_LABELS`** to `wip`. This will prevent any PR with the `wip` label from being merged.
- Your SRE team requests that all PRs get marked as either high- or low-risk before being merged, so that if the site goes down or something is wrong, they can quickly scan for changes that developers anticipated might have adverse effects.
    - **`REQUIRED_LABELS_ANY`**: `high-risk,low-risk`. This will require at least one of `high-risk` or `low-risk` to be added to the PR before it can be merged.

---

## Easy Installation

### Deploy to Heroku

Click the following button to deploy this app to heroku (you'll need a heroku account):

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

You'll be presented with a set-up screen.

Enter the name for your app. Something like `your-required-labels`.

Set up the required labels (comma separated):

- `REQUIRED_LABELS_ANY`: At least one of these labels should be present on all PRs
- `REQUIRED_LABELS_ALL`: All of these labels must be present on all PRs
- `BANNED_LABELS`: None of these labels can be present on all PRs

Enter the credentials:

- `GITHUB_TOKEN`: A github user TOKEN for user that will post the status. We suggest you create a dummy github user for this purpose. This user *must* have permission to write to the repo in order for it to post a status.

**OR**

- `GITHUB_USER`: The username of the GitHub user that will post the status. We suggest you create a dummy github user for this purpose. This user *must* have permission to write to the repo in order for it to post a status.
- `GITHUB_PW`: The password for this GitHub user.

> Note: The application will use GITHUB_TOKEN first if defined and will fall back to GITHUB_USER and GITHUB_PW if not.

Click "deploy app". The app will deploy.

When completed, you can click "Launch App" and it will take you to an information screen which lists all of the label settings.

Next, you should [set up your repo](#set-up-your-repo).

### Updating label settings

In the [heroku dashboard](https://dashboard.heroku.com) for your app, click `Settings` then `Reveal Config Vars`. Here you will be able to update the label settings and github credentials at any time.


## Deploy to your own machine

### Dependencies
- python 3
- pip

### Installation

- Clone this repo:

```sh
$ git clone git@github.com:dimagi/required-labels.git
```

- Install the dependencies

```sh
$ pip install -r requirements.txt
```

- Create a config file

```sh
$ cp custom.conf.template custom.conf
```
Then modify `custom.conf` with your own settings.
Default behavior is to source this file from project cloned directory.

You can source a custom file path using `CONFIG_FILE` environment variable.

```sh
$ export CONFIG_FILE=/some/path/to/config.conf
```

You can also set `REQUIRED_LABELS_ALL`, `REQUIRED_LABELS_ANY`, or `BANNED_LABELS` along with `GITHUB_USER` and `GITHUB_PW` directly as environment variables:

```sh
$ export REQUIRED_LABELS_ALL=required-label-name,other-required-label-name
$ export GITHUB_USER={username}
$ export GITHUB_PW={password}
```

- Run the app

```sh
$ gunicorn main:app
```


## Set up your repo

### Enable the Webhook
In the GitHub repository you want to enable this service, click `Settings` -> `Webhooks` -> `Add Webhook`. Then enter the following settings:

- **Payload URL**: The URL to your heroku app. e.g. https://your-required-labels.herokuapp.com
- **Content Type**: "application/json"
- **Let me select individual events**: Set this to "Pull Request" only.
- **Active**: Leave this selected.

[<img src="https://user-images.githubusercontent.com/146896/34696493-0dec922a-f49d-11e7-8f30-0d27f7c5a8c8.png" width="295">](https://user-images.githubusercontent.com/146896/34696493-0dec922a-f49d-11e7-8f30-0d27f7c5a8c8.png)

Now, a new "checker" should show up when creating a new pull request.
![Label requirements satisfied](https://user-images.githubusercontent.com/146896/34694324-a926ebfe-f494-11e7-983f-b10e10719c83.png)

### Ensure the user has write permissions

In the `Collaborators & teams` settings page, make sure the user who you set up earlier has at least `Write` permissions on the repo.

## Running Tests

```sh
$ python -m unittest -v
```
