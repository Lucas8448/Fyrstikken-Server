import json
import os
from fpdf import FPDF
import random
import string

user_count = 20

folder = './storage/users/'

def randomstring():
  return ''.join(random.choice(string.ascii_letters) for i in range(8))

def create_users():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size = 12)

    positions = [(x, y) for x in [10, 110] for y in range(20, 280, 70)]
    user_position = 0
    for i in range(user_count):
        username = randomstring()
        password = randomstring()

        with open(os.path.join(folder, username + '.json'), 'w') as f:
            json.dump({
                'username': username, 
                'password': password, 
                'voted': False, 
                'votes': {
                    str(j): 0 for j in range(1, 14)
                }
            }, f)
        
        x, y = positions[user_position]
        pdf.set_xy(x, y)
        pdf.multi_cell(80, 10, txt = "Brukernavn: " + username, border=1)
        pdf.set_xy(x, y + 10)
        pdf.multi_cell(80, 10, txt = "Passord: " + password, border=1)

        user_position += 1
        if user_position == len(positions):
            pdf.add_page()
            user_position = 0

        print("Created user " + str(i + 1) + " of " + str(user_count))

    pdf.output(os.path.join('./storage/pdfs/', 'users.pdf'))

create_users()