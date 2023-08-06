from urllib import request
from argparse import ArgumentParser
from json import loads
from datetime import datetime


def init_parser():
    parser = ArgumentParser(prog="CowinCLI",
                            description="Get information about centers and vaccine availability")
    parser.add_argument('-pincode', default=670601,
                        type=int, help="Pincode of the region")
    return parser


def get_centers(url: str):
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/90.0.4430.212 Safari/537.36",
        "Accept": "application/json, text/plain, */*"
    }
    req = request.Request(url, headers=header)
    resp = request.urlopen(req).read()
    content = loads(resp.decode('utf-8'))
    return json_parser(content)


def json_parser(data: dict):
    if not data['centers']:
        return "No centers found in your locality"
    data = data['centers'][0]
    return f"""
    {data['name']} - {data['state_name']}, {data['district_name']}, {data['block_name']}
    At: {data['address']}
    Time: {data['from'][:-3]}-{data['to'][:-3]}
    Type: {data['fee_type']}
    Sessions: {len(data['sessions'])}
    Available: {data['sessions'][0]['available_capacity']}
    """


def today():
    return datetime.strftime(datetime.today(), "%d-%m-%y")


class CowinCLI:

    def __init__(self):
        parser = init_parser()
        args = parser.parse_args()
        self.pincode = args.pincode
        self.run()

    def run(self):
        url = f"https://cdn-api.co-vin.in/api/v2/appointment/" \
              f"sessions/public/calendarByPin" \
              f"?pincode={self.pincode}&date={today()}"
        res = get_centers(url)
        print(res)


if __name__ == '__main__':
    CowinCLI()
