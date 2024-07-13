from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage,AIMessage
load_dotenv()

llm=ChatGoogleGenerativeAI(model="gemini-1.5-pro")

out=StrOutputParser()
Chat_history=[]

sys="""you are a chat bot in a pizzeria.you have to intract with the customer to help them by answering their queries regarding items in the
    menu{menu}, amount  etc.you have to take orders from the customers 
    based on the menu . Based on the order from customer, you need to sum the total amount and communicate
    to the customer for that you can use {Chat_history} only when they are done or asking for the total amount
    .If the item is not available in the menu, you need to tell the customer that the 'Item is not available' and then show them the menu in an attractive way. 
    and ask user to pick from the options you have. for pizzas and drinks like coke,sprite etc where i provided multiple rates:the menu contains price for each size large,medium,small respectively ,
    same goes for fries but have large and small respectively , 
    bottled water & toppings have their own prices per piece/topping, 
    When user say they want any kind of pizza do remind them that they can choose toppings.After all this you have to count the final amount and display it
    if the customer any thing else just respond in a good way use emojis to make the conversation good
    if anything the user ask that is not in your knowledge 'sorry i am not trained to answer that
    """
Prompt=ChatPromptTemplate.from_messages(
    [
        ("system",sys),
        ("user","{order}")
    ]
)


menu={"Pizza":{
		"pepperoni pizza" :[ 12.95, 10.00, 7.00] ,
		"cheese pizza" :  [10.95, 9.25, 6.50] ,
		"eggplant pizza"  : [11.95, 9.75, 6.75] },
	"Extras":{
        "fries": [4.50, 3.50] ,
		"greek salad": 7.25 },
	"Toppings": {
		"extra cheese": 2.00, 
		'mushrooms' :1.50 ,
		'sausage' :3.00 ,
		'canadian bacon': 3.50 ,
		"sauce" :1.50 ,
		"peppers": 1.00 ,
		},
	"Drinks": {
		"coke": [3.00, 2.00, 1.00 ],
		"sprite": [3.00, 2.00, 1.00 ],
		"bottled water" :5.00 ,
		}
}
chain= Prompt | llm | out
def getorder(customer):
    result=chain.invoke({"Chat_history":Chat_history,"order":customer,"menu":menu})
    return(result)

while True:
    ask=input(">>")
    if ask=="quit":
        break
    ai_resp=getorder(ask)
    print(">>",ai_resp)
    Chat_history.append(HumanMessage(content=ask))
    Chat_history.append(AIMessage(content=ai_resp))
   


    
		
