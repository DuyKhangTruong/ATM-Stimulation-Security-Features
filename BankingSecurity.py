#Product of Khang Nguyen

# Import openCv module
import cv2
import smtplib
import ssl
import numpy as np
from threading import Thread
import asyncio
import codecs
import certifi


class Banking_Security:
    def __init__(self):
        self.Id = '123456789'
        self.password = '14092015'
        self.balance = 25000
        self.counting = 0
        self.check = False

# Checking information of clients
    def Checking_Procedure(self, loop):
        UserName = input('Please type your Id: ')
        Password = input('Please type your password: ')
        while True:

            if UserName == self.Id and Password == self.password:
                print('You have logined successfully')
                self.Banking_Menu()
                break
            elif UserName == self.Id and (Password == 'Forget'):
                answer = input('Do you want to change your password: ')
                if answer.startswith('y'):
                    self.password = input('please type your new password: ')
                    self.Checking_Procedure()
                else:
                    break
            else:
                print('Your UserName or password is wrong.Please type again')
                UserName = input('Please type your Id: ')
                password = input('Please type your password again: ')
                self.counting += 1
                if self.counting > 1:
                    self.SendingEmail()
                    print(
                        'You have tried so many times and security procedure has turned on')
                    # Security_Procedure()
                    print('Your account has been blocked')
                    self.check = True
                    break
        return self.check

    def Banking_Menu(self):
        print('Please select your options')
        print('Option 1: Withdraw or deposite')
        print('Option 2: Account information')
        print('Option 3: Transaction')
        ans = input('Your option: ')
        while True:
            if ans == '1':
                self.Withdraw_Deposite()
                break
            elif ans == '2':
                self.AccountInformation()
                break
            elif ans == '3':
                self.Transaction()
                break
            else:
                ans = input('Please choose your option again: ')

    def Security_Procedure(self):
        # Create the haar cascade
        faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_alt2.xml')
        video_capture = cv2.VideoCapture(0)

        while True:
            # Capture frame-by-frame
            ret, frame = video_capture.read()

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            faces = faceCascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30),
                flags=cv2.CASCADE_SCALE_IMAGE
            )

            # Draw a rectangle around the faces
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)

            cv2.imshow('Video', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        video_capture.release()
        cv2.destroyAllWindows()

        # Add this one if the window is freeze
        for i in range(1, 2):
            cv2.waitKey(1)

    def VideoRecording(self):
        pass

    def SendingEmail(self):
        port = 587  # For starttls
        smtp_server = "smtp.gmail.com"
        sender_email = "khangtest23@gmail.com"
        receiver_email = "khanganddoublelift@gmail.com@gmail.com"
        password = "testing23"

        context = ssl.create_default_context()
        message = """\
        Subject: Warning

        Someone is trying to access to your bank account."""

        context = ssl.create_default_context()
        with smtplib.SMTP(smtp_server, port) as server:
            server.ehlo()  # Can be omitted
            server.starttls(context=context)
            server.ehlo()  # Can be omitted
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)

    def Again(self):
        print('Do you want to do another task (yes or no)')
        return input().startswith('y')

    def Withdraw_Deposite(self):
        Ans = input('Would you like to withdraw or deposite: ')
        while True:
            if Ans == 'withdraw':
                withdraw = int(input('Please type your withdraw amount: '))
                if withdraw <= self.balance:
                    print('You have withdrawed successfully')
                    print('Balance: %s' % (self.balance - withdraw))
                    break
                else:
                    print('Your balance is not sufficient for the withdraw: ')
            elif Ans == 'deposite':
                if input('Please type your password: ') == self.password:
                    deposite = int(
                        input('Please type the amount you want to deposite: '))
                    self.balance += deposite
                    print('You have deposited successfully', end=' ')
                    print('Balance: %s' % (self.balance))
                    break
            else:
                Ans = input('Please type correctly: ')

        if input('Do you want to continue: ').startswith('y'):
            self.Withdraw_Deposite()
        else:
            if self.Again():
                self.Banking_Menu()
            else:
                quit()

    def AccountInformation(self):
        print('Bank account: %s ' % (self.Id), end=' ')
        print('  Balance: %s' % (self.balance))
        if self.Again():
            self.Banking_Menu()
        else:
            quit()

    def Transaction(self):
        transaction = int(input('Please input the amount you want to send: '))
        while transaction > self.balance:
            print('This transaction can not be processed')
            if input('Do you want to make another transaction (yes or no): ').startswith('y'):
                self.Transaction()
            else:
                break

        receiver = input('Please type the bank account you want to send to: ')
        print('The transaction has been processed successfully')
        print('Receiver: %s' % (receiver), end='')
        print(' Transaction: %s' % (transaction))
        self.balance -= transaction
        print('Balance: %s' % (self.balance))

        if self.Again():
            self.Banking_Menu()
        else:
            quit()


if __name__ == "__main__":
    testing = Banking_Security()
    loop = asyncio.new_event_loop()

    t1 = Thread(target=testing.Checking_Procedure, args=(loop,))
    t1.start()

    t2 = Thread(target=testing.Security_Procedure())
    t2.start()

    if testing.check:
        if not testing.Again():
            quit()
