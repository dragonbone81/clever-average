import requests


class Clever(object):
    def __init__(self):
        self.base_url = "https://api.clever.com"
        self.students = 0
        self.sections = 0

    def calculate_avg_students_section(self):
        """
        calculates the average students in a section
        :return:
        """
        response = requests.get(self.base_url + '/v2.0/sections', headers={'Authorization': 'Bearer DEMO_TOKEN'}).json()
        self.sections += self.get_sections(response)
        self.students += self.get_students(response)

        while response.get('next') or response.get('links'):
            if response.get('next'):
                response = requests.get(self.base_url + response.get('uri'),
                                        headers={'Authorization': 'Bearer DEMO_TOKEN'}).json()
            if response.get('links'):
                url_next = None
                for url in response.get('links'):
                    if url.get('rel') == 'next':
                        url_next = str(url.get('uri'))
                if url_next:
                    response = requests.get(self.base_url + url_next,
                                            headers={'Authorization': 'Bearer DEMO_TOKEN'}).json()
                else:
                    self.sections += self.get_sections(response)
                    self.students += self.get_students(response)
                    break
            self.sections += self.get_sections(response)
            self.students += self.get_students(response)
        return self.students / self.sections

    def get_sections(self, response):
        return len(response.get('data'))

    def get_students(self, response):
        students = 0
        for section in response.get('data'):
            students += len(section.get('data')['students'])
        return students


if __name__ == "__main__":
    clever = Clever()
    print(clever.calculate_avg_students_section())
