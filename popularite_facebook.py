from robobrowser import RoboBrowser



class Bowser:
    def __init__(self):
        self.b = RoboBrowser()
        self.connexion()

    def connexion(self):
        self.b.open('http://facebook.com')
        form = self.b.get_form(id="login_form")
        form["email"] = "A.andy@hotmail.fr"
        form["pass"] = "p3Ace70v3ook"
        form.serialize()
        self.b.submit_form(form)

    def run(self):
        self.b.open("https://www.facebook.com/pg/JLMelenchon/community/?ref=page_internal")
        print(str(self.b.select)[:1000])
        # Impossible d'acceder aux commentaires...


if __name__ == "__main__":
    B = Bowser()
    B.run()

    
