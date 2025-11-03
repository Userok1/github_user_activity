# C:\Users\Gwyn\Desktop\python\learning\common_python\github_user_activity\github_user_activity

import requests
from argparse import ArgumentParser


headers = {
    "Accept": "application/vnd.github+json",
}
params = {
    "Per_page": "10" 
}


class Cli:
    def __init__(self):
        self.parser = Cli.__create_parser()


    def run(self):
        try:
            while True:
                user_input = input(">> ")
                try:
                    self.gh_request(user_input)
                except SystemExit:
                    continue
                except UserWarning:
                    print("No such user")
                    continue
        except KeyboardInterrupt:
            print("\nEnd of program")


    def gh_request(self, user_input: str) -> tuple[dict[str, tuple], str]:
        username = self.handle_command(user_input.strip())
        url = Cli.__get_url(username)
        r = requests.get(url=url, params=params, headers=headers)
        if r.status_code != 200:
            raise UserWarning
        user_info = Cli.__handle_reponse(r.json())
        Cli.__pretty_info(user_info)


    def handle_command(self, user_input: str) -> str:
        user_input = user_input.split()

        args = self.parser.parse_args(user_input)
        if args.command:
            if args.username and type(args.username) == str:
                username = args.username

                return username
            else:
                raise UserWarning
        else:
            raise UserWarning


    @staticmethod
    def __create_parser() -> ArgumentParser:
        parser = ArgumentParser(description="The CLI interface to track github user's last events")
        subparsers = parser.add_subparsers(dest="command")

        github_activity_parser = subparsers.add_parser("github-activity",
                                                       help="Github-activity command to track user's events")
        github_activity_parser.add_argument("username",
                                            help="username of github user to track")
        
        return parser


    @staticmethod
    def __get_url(username: str) -> str:
        url = f"https://api.github.com/users/{username}/events"
        return url
    

    @staticmethod
    def __handle_reponse(data: dict[str, str]) -> dict[str, list[str, int]]:
        
        activity = {}
        
        for user in data:
            repo_name, event_type = user['repo']['name'], user['type']
            if event_type in ("PushEvent", "WatchEvent"):
                if repo_name not in activity.keys():
                    activity[repo_name] = [event_type, 1]
                else:
                    activity[repo_name][1] += 1
        
        return activity
    

    @staticmethod
    def __pretty_info(info: dict[str, list]) -> list:
        
        result_list = []

        for repo_name, event_list in info.items():
            if event_list[0] == "WatchEvent":
                s = f"Starred {repo_name}"
                result_list.append(s)
            elif event_list[0] == "PushEvent":
                s = f"Pushed {event_list[1]} commits to {repo_name}"
                result_list.append(s)

        for a in result_list:
            print(a)
        

if __name__ == "__main__":
    cli = Cli()
    cli.run()