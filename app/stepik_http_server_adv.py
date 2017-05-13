import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
import requests

simple_dao_dict = {}  # store list of (lesson_id, theor_steps_list)


def get_stepik_lesson_json(n: str or int) -> str:
    """
    Get json description of lesson n 
    :param n: lesson id
    :return: json txt
    """
    link = f'https://stepik.org/api/lessons/{n}'
    response = requests.get(link).json()
    return response


def get_stepik_step_json(step_id: str) -> str:
    """
    Get json description of step step_id 
    :param step_id: step id
    :return: json txt
    """
    link = f'https://stepik.org/api/steps/{step_id}'
    response = requests.get(link).json()
    return response


def get_update_date(date_txt: str) -> datetime.datetime:
    """
    Convert date_txt to datetime.datetime
    :param date_txt: 
    :return: datetime.datetime
    """
    return datetime.datetime.strptime(date_txt, "%Y-%m-%dT%H:%M:%SZ")


def get_theor_steps(lesson_id: str or int) -> (str, bool):
    """
    Get theoretical steps id list json txt
    :param lesson_id: str or int
    :return: json of ids and bool success status    
    """
    try:
        lesson = get_stepik_lesson_json(lesson_id)  # lesson json
        theor_steps = []  # list of theor steps id
        all_steps = lesson['lessons'][0]['steps']  # all steps of lesson

        for step_id in all_steps:
            step = get_stepik_step_json(step_id)  # cur step json
            if len(step['steps'][0]['actions']) == 0:  # if 'action': {} is theoretical step
                theor_steps.append(step_id)
                # update_date = get_update_date(step['steps'][0]['update_date'])

        if len(theor_steps) == 0:
            return 'Theoretical steps not found', False
        else:
            # compose json output str
            theor_steps_str = ', '.join(map(str, theor_steps))
            output_json = "{'id': " + theor_steps_str + "}"
            return output_json, True

    except Exception as ex:
        return ex, False


class MyHTTPServerRequestHandler(BaseHTTPRequestHandler):
    """Class for http server"""
    def do_GET(self):
        """
        Process get request
        write response message
        """
        global simple_dao_dict

        self.send_response(200) # status OK
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        # get input parameters as list of str
        # ['a=1', 'b=2', 'c=3', 'lesson=7121']
        path_items = [i for i in urlparse(self.path).query.split('&') if len(i) > 0 and '=' in i]

        if len(path_items) > 0:
            print(path_items)
            # create parameters dict
            parameters_dict = {cmd.split('=')[0]: cmd.split('=')[1] for cmd in path_items}

            n = parameters_dict['lesson']  # get lesson parameter as str
            print('lesson for analysis: ', n)

            if n not in simple_dao_dict:
                # start searching if do not have value in simple_dao_dict
                message, success_status = get_theor_steps(n)  # get json with ids of theor steps
                if success_status:  # if all right add (n, message) to simple_dao
                    simple_dao_dict.update({n: message})
            else:
                # if we already have answer we get it from simple_dao_dict
                message = simple_dao_dict[n]
                print('we already have it!')

            self.wfile.write(bytes(message, "utf8"))  # write output message

        return


def run():
    """Start server"""
    print('stepik task starting server...')
    server_address = ('127.0.0.1', 8081)
    httpd = HTTPServer(server_address, MyHTTPServerRequestHandler)
    print('running...')
    httpd.serve_forever()  # main loop


if __name__ == '__main__':
    run()
