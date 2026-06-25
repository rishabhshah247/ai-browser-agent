import asyncio  # Asynchronous features use karne ke liye library
import json     # JSON file ko padhne ke liye library

# Yeh hamara main async function hai jo data padhega
async def read_memory():
    # 'open' command file ko kholta hai, 'r' ka matlab read mode
    with open("user_info.json", "r") as file:
        # json.load us text file ko Python ki dictionary mein convert karta hai
        data = json.load(file)
    
    # \n se ek empty line aati hai. Hum apna data nicely print kar rahe hain
    print("\n--- USER MEMORY LOADED ---")
    
    # data['name'] ka matlab hai dictionary se 'name' ki value uthao
    print(f"Name: {data['name']}")
    print(f"Email: {data['email']}")
    print(f"Phone: {data['phone']}")
    print(f"Address: {data['address']}")
    
    # Ek artificial delay daal rahe hain takki hum dikha sakein ki await kaise kaam karta hai
    # Yeh 1 second tak wait karega bina system ko hang kiye
    await asyncio.sleep(1)
    
    print("--------------------------\n")

# Yeh entry point hai, har program ka ek main block hota hai
async def main():
    print("Agent is waking up...")
    # await lagana padta hai jab bhi koi async function call karte hain
    await read_memory()
    print("Agent is ready!")

# Yeh line check karti hai ki hum file ko direct chala rahe hain ya kahin aur se import kar rahe hain
if __name__ == "__main__":
    # asyncio.run() Event Loop ko start karta hai aur hamare main() function ko chalata hai
    asyncio.run(main())