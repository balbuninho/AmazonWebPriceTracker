import requests
import bs4
import smtplib
import time


def main():
    # get user data

    print('Give me product to track')
    url = get_url()
    print('Give me your e-mail')
    notification = notification_email_address()
    print('Give me price to compare with')
    price_to_check = get_value_to_check()

    print('Give me e-mail login & password to send an e-mail with notification')
    log = get_login_to_email()
    password = get_mail_password()
    print('Enter how many times you want to check price per day'
          '1 = 86400'
          '2 = 43200'
          '6 = 14400'
          'Every hour = 3600')
    value = get_time()

    # default headers

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/80.0.3987.122 Safari/537.36'}
    # compare price

    while True:
        check_for_price_reduction(url, headers, price_to_check, log, password, notification)
        time.sleep(value)


def check_for_price_reduction(url, headers, price_to_check, log, password, notification):

    page = requests.get(url, headers=headers)

    plain_text = page.text

    soup = bs4.BeautifulSoup(plain_text, 'html.parser')

    price = soup.find(id='priceblock_ourprice').get_text()

    convert_price = price[:-5]

    price_to_compare = float(convert_price)

    if price_to_compare < price_to_check:
        send_mail(url, log, password, notification)


def get_url():

    url = input('Enter URL address: ')
    return url


def get_value_to_check():
    value = float(input('Enter price to compare: '))
    return value


def notification_email_address():
    address = input('Enter your e-mail address: ')
    return address


def get_login_to_email():
    login = input('Enter login to  e-mail account: ')
    return login


def get_mail_password():
    password = input('Enter password to e-mail account: ')
    return password


def get_time():
    tim = input('Enter value:')
    convert = float(tim)
    return convert


def send_mail(url, login, password, notification_address):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(login, password)
    mail_subject = 'Price is reduced! '
    mail_body = 'Check the link! '
    message = f'Subject: {mail_subject}\n\n{mail_body}\n\n{url}'
    server.sendmail(
        login,
        notification_address,
        message)
    server.quit()
    print('E-mail has been send to')


if __name__ == '__main__':
    main()
