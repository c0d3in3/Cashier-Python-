class Cashier():

    receipt = []
    receipt_money = 0

    def __init__(self, reciept, reciept_money):
        self.self = self


    @classmethod
    def showProducts(self):

        database = open("database.txt", "r")

        for line in database:
            if (line[0] == "#"):
                continue

            splitted = line.split(";")

            print("პროდუქტის კოდი: {}. პროდუქტი: {}. ფასი: {} ლარი. ხელმისაწვდომია: {}  ცალი/კგ".format(splitted[0],
                                                                                                        splitted[1],
                                                                                                        splitted[2],
                                                                                                        splitted[3]))
        value = input("თუ გსურთ პროდუქტის შეძენა შეიყვანეთ პროდუქტის კოდი: ")
        Cashier.sellProduct(value)

    @classmethod
    def sellProduct(self, code):

        success = False
        database = open("database.txt", "r+")

        for line in database:

            if (line[0] == "#"):
                continue

            splitted = line.split(";")

            if (int(splitted[0]) == int(code)):
                success = True
                quantity = int(input("რამდენის ყიდვა გსურთ? (ხელმისაწვდომია: {} ცალი/კგ) : ".format(splitted[3])))

                try:
                    if (quantity > int(splitted[3]) or quantity == 0):
                        Cashier.sellProduct(code)
                        return True
                except ValueError:
                    print("შეიყვანეთ ნატურალური რიცხვი")

                if (int(splitted[4]) > 0):
                    promo = input("ამ პროდუქტზე მოქმედებს პრომო კოდი, თუ იცით შეიყვანეთ, თუ არა დატოვეთ ცარიელი: ")


                    if (promo == ""):
                        print("თქვენ წარმატებით შეიძინეთ {} {} ცალი/კგ {} ლარად!".format(splitted[1], quantity,
                                                                                         float(splitted[2]) * quantity))

                    elif (int(promo) == int(splitted[4]) and promo != ""):
                        self.reciept_money += (float(splitted[2]) - float(splitted[5])) * quantity
                        self.reciept.append([splitted[1], quantity, (float(
                                splitted[2]) - float(splitted[5])) * quantity])
                        print("თქვენ წარმატებით შეიძინეთ {} {} ცალი/კგ ფასდაკლებით {} ლარად!".format(splitted[1],
                                                                                                     quantity, (float(
                                splitted[2]) - float(splitted[5])) * quantity))

                    else:
                        print("პრომო კოდი არასწორია!")
                        self.reciept_money += float(splitted[2]) * quantity
                        self.reciept.append([splitted[1], quantity, float(splitted[2]) * quantity])
                        print("თქვენ წარმატებით შეიძინეთ {} {} ცალი/კგ {} ლარად!".format(splitted[1], quantity,
                                                                                         float(splitted[2]) * quantity))

                else:
                    Cashier.receipt_money += float(splitted[2]) * quantity
                    Cashier.receipt.append([splitted[1], quantity, float(splitted[2]) * quantity])
                    print("თქვენ წარმატებით შეიძინეთ {} {} ცალი/კგ {} ლარად!".format(splitted[1], quantity,
                                                                                     float(splitted[2]) * quantity))


                splitted[3] = int(splitted[3]) - quantity
                for i, item in enumerate(splitted):
                    if (i == 5):
                        continue
                    splitted[i] = str(item) + ";"
                new_line = "".join(str(i) for i in splitted)
                Cashier.updateDatabase(code, new_line)
                user_value = input("გსურთ ყიდვის გაგრძელება? (თანხმობისთვის yes, უარყოფისთვის no): ")
                if(user_value == "yes"):
                    Cashier.showProducts()
                else:
                    Cashier.showReciept()
                break

        if (success == False):
            print("პროდუქტი ამ კოდით ვერ მოიძებნა!")
        database.close()

    @classmethod
    def updateDatabase(self, code, update):
        with open('database.txt', 'r+') as database:
            data = database.readlines()
            database.seek(0)
            for line in data:
                if (line[0] == "#"):
                    database.write(line)
                    continue
                splitted = line.split(";")
                if int(float(splitted[0])) != int(code):
                    database.write(line)
            database.write(update)
            database.truncate()

    @classmethod
    def showReciept(self):
        print(Cashier.receipt)
        print("==============ჩეკი==============\n\n")
        for item in Cashier.receipt:
            print("{} {} ცალი/კგ - {} ლარი".format(item[0], item[1], item[2]))
        print("გადასახდელია: {} ლარი".format(Cashier.receipt_money))
        print("===============================\n\n")
