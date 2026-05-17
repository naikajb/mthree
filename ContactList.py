contacts = {
    1: {
        "first_name": 'naika',
        "last_name": 'jb',
        "phone": "(450)-123-4567",
        "email": "naika1492@gmail.com",
        "address": "1234 Main St",
        "city": "Anytown",
        "state": "CA",
        "zip": "12345",
        "birthdate": "1990-01-01"
    }
}

def print_contact(contact_list):
    # if its list of contacts, print each contact info, otherwise print the single contact info
    if isinstance(contact_list, dict):
        for idx in contact_list:
            print(f"Contact ID: {idx}")
            print(f"    Name: {contact_list[idx]['first_name']} {contact_list[idx]['last_name']}")
            print(f"    Phone: {contact_list[idx]['phone']}")
            print(f"    Email: {contact_list[idx]['email']}")
            print(f"    Address: {contact_list[idx]['address']}, {contact_list[idx]['city']}, {contact_list[idx]['state']} {contact_list[idx]['zip']}")
            print(f"    Birthdate: {contact_list[idx]['birthdate']}")
            print("-----------------------------")
    

def next_id(): 
    return max(contacts.keys(), default=0) + 1

def add_contact():
    print("\n--------Add New Contact---------")
    firstname   = input("First Name:     ").strip()
    lastname    = input("Last Name:      ").strip()
    phone       = input("Phone Number (xxx)-xxx-xxxx:   ").strip()
    email       = input("Email (ex: email@address.com)  ").strip()
    birthdate   = input("Birthday(ex YYYY-MM-DD):       ").strip()

    address   = input("Address:    ").strip()
    city      = input("City:       ").strip()
    state     = input("State:      ").strip()
    zip_code  = input("Zip:        ").strip()


    new_contact = {
        "first_name" : firstname,
        "last_name" : lastname,
        "phone":      phone,
        "email":      email,
        "birthdate":  birthdate,
        "address":    address,
        "city":       city,
        "state":      state,
        "zip":        zip_code,
    }

    contact_id = next_id()
    contacts[contact_id] = new_contact
    print(f"New Contact was added for {firstname} {lastname}. See Contact Info below : \n {print_contact({contact_id: contacts[contact_id]})}")

def list_contacts():
    for idx in contacts:
        print(f"{idx}. {contacts[idx]['last_name']}, {contacts[idx]['first_name']} ")
    

def view_contact():
    options = {
        "1": "Phone",
        "2": "Full Name",
        "3": "First Name",
        "4": "Last Name",
        "5": "Back to Menu",
    }

    print("How do you want to look up this contact?")
    for key in options:
            print(f"{key}. {options[key]}")

    method = input("Look up method: ")
    
    if method not in options:
        print("Invalid option. Back to menu")
    
    found_contacts = None
    if method == "1":
        found_contacts = lookup('phone', input("Number: "))
    elif method == "2":
        found_contacts = lookup("full", input("Full Name: "))
    elif method == "3":
        found_contacts =  lookup('first_name', input("First Name: "))
    elif method == "4":
        found_contacts = lookup('last_name', input("Last Name: "))
    elif method == "5":
        found_contacts = lookup('email', input("Email: "))
    else:
        print("Back to menu")
    
    if found_contacts is None:
        print("Contact not found. Back to menu.")
    else:
        print("Contact found:")
        print_contact(found_contacts)
        



def lookup(method, str):
    results = {}
    if method == "full":
        for idx in contacts:
            full_name = f"{contacts[idx]['first_name']} {contacts[idx]['last_name']}"
            if full_name == str:
                results[idx] = contacts[idx]   
    else:
        for idx in contacts:
            if contacts[idx][method] == str:
               results[idx] = contacts[idx]
    return results if results else None
                

def update_contact():
    # ask for name and last name, 
    print("To update a contact, please provide the first and last name.")
    input_name = input("First Name: ").strip()
    input_last_name = input("Last Name: ").strip()
    
    # find the contact,
    print(f"\nLooking up info for {input_name} {input_last_name} .......")
    found_contacts = lookup("full", f"{input_name} {input_last_name}")

    # if found, print the contact info,
    if found_contacts is None:
        print("No matching contact found.")
        return
    else:
        if len(found_contacts) > 1:
            print(f"Multiple contacts found for {input_name} {input_last_name}. See below: \n") 
            print(f"Contact(s) found for {input_name} {input_last_name}: \n")
            
            # if duplicate found, ask for phone number to narrow down the search,
            print("Please provide the phone number to narrow down the search.")
            phone_number = input("Phone Number: ").strip()
            found_contacts = lookup("phone", phone_number)

            if found_contacts is None:
                print("No matching contact found with that phone number. Back to menu.")
            else:
                print("Contact found:")
                print_contact(found_contacts)
        else:
            print_contact(found_contacts)
    
    field_options = {
        "1": "first_name",
        "2": "last_name",
        "3": "phone",
        "4": "email",
        "5": "address",
        "6": "city",
        "7": "state",
        "8": "zip",
        "9": "birthdate",
        "10": "Back to Menu"
    }

    # ask which field to update,
    print("Which field do you want to update?")
    for key in field_options:
        print(f"{key}. {field_options[key]}")
    input_field = input("Which field do you want to update? (1-10): ").strip()
    if input_field not in field_options:
        print("Invalid option. Back to menu.")
        return
    else:
        if input_field == "10":
            print("Back to menu.")
            return
        else:
            # ask for new value, 
            new_value = input(f"Enter new value for {field_options[input_field]}: ").strip()
            for idx in found_contacts:
                contacts[idx][field_options[input_field]] = new_value

            # update the contact
            print("Contact updated successfully. See updated contact info below: \n")
            print_contact(found_contacts)


def del_contact():
    print("To delete a contact, please provide the first and last name.")
    input_name = input("First Name: ").strip()
    input_last_name = input("Last Name: ").strip()
    
    print(f"\nLooking up info for {input_name} {input_last_name} .......")
    found_contacts = lookup("full", f"{input_name} {input_last_name}")

    if found_contacts is None:
        print("No matching contact found.")
        return
    else:
        if len(found_contacts) > 1:
            print(f"Multiple contacts found for {input_name} {input_last_name}. See below: \n") 
            print(f"Contact(s) found for {input_name} {input_last_name}: \n")
            
            print("Please provide the phone number to narrow down the search.")
            phone_number = input("Phone Number: ").strip()
            found_contacts = lookup("phone", phone_number)

            if found_contacts is None:
                print("No matching contact found with that phone number. Back to menu.")
                return
            else:
                print("Contact found:")
                print_contact(found_contacts)
        else:
            print_contact(found_contacts)
    
    confirm = input("Are you sure you want to delete this contact? (y/n): ").strip().lower()
    if confirm == "y":
        for idx in found_contacts:
            del contacts[idx]
        print("Contact deleted successfully. Back to menu.")
    else:
        print("Deletion cancelled. Back to menu.")


def menu():

    options = {
        "1": ("Add Contact", add_contact),
        "2": ("List All Contacts", list_contacts ),
        "3": ("View A Contact", view_contact),
        "4": ("Update A Contact", update_contact),
        "5": ("Delete A Contact",del_contact),
        "6": ("Exit", None)
    }

    while True: 
        print("====== Contact List ======")
        for key, (label, _) in options.items():
            print(f"{key}.{label}")

        print("==========================")
        choice = input("CHOOSE AN OPTION: ").strip() 

        if choice not in options:
            print("Invalid option, try again.")
            continue

        label, action = options[choice]
        if action is None:
            print("Goodbye!")
            break
        action()


if __name__ == "__main__":
    menu()