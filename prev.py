import subprocess


class PasswordRevealer:
    def __init__(self):
        self.__meta_data: any = subprocess.check_output(["netsh", "wlan", "show", "profiles"])
        self.__data = self.meta_data.decode("utf-8", errors="backslashreplace").split("\n")
        self.__profiles = []

    @property
    def meta_data(self):
        return self.__meta_data

    @property
    def profiles(self):
        return self.__profiles

    @property
    def data(self):
        return self.__data

    # traverse the data
    def traverse_data(self):
        for i in self.data:
            # find "All User Profile" in each item
            if "All User Profile" in i:
                # if found
                # split the item
                i = i.split(":")
                # item at index 1 will be the Wi-Fi name
                i = i[1]
                # formatting the name
                # first and last character is use less
                i = i[1:-1]
                # appending the Wi-Fi name in the list
                self.profiles.append(i)

    # display profiles
    def display_profiles(self):
        # printing heading
        print("{:<30}| {:<}".format("Wi-Fi Name", "Password"))
        print("----------------------------------------------")
        # traversing the profiles
        for i in self.profiles:
            # try catch block begins
            # try block
            try:
                # getting meta_data with password using Wi-Fi name
                results = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', i, 'key=clear'])
                # decoding and splitting data line by line
                results = results.decode('utf-8', errors="backslashreplace")
                results = results.split('\n')
                # finding password from the result list
                results = [b.split(":")[1][1:-1] for b in results if "Key Content" in b]
                # if there is password it will print the pass word
                try:
                    print("{:<30}| {:<}".format(i, results[0]))
                # else it will print blank in front of pass word
                except IndexError:
                    print("{:<30}| {:<}".format(i, ""))
            # except block
            except subprocess.CalledProcessError:
                # if there is any error
                # it will print error
                print("ERROR")
                continue

    # str method
    def __str__(self):
        return f"PasswordRevealer({self.profiles})"


def main():
    password_revealer = PasswordRevealer()
    password_revealer.traverse_data()
    password_revealer.display_profiles()


if __name__ == "__main__":
    main()