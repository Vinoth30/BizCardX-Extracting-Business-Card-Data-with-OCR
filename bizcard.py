# Libraries Used
import pymysql
import pandas as pd
import matplotlib.pyplot as plt
import easyocr
from easyocr import Reader
from PIL import Image
import cv2
import os
from datetime import datetime
import streamlit as st
from streamlit_option_menu import option_menu
import re

# Streamlit Page Setiings
st.set_page_config(page_title="BizCardX - Business Card Data Extraction with OCR",
                   layout="wide",
                   initial_sidebar_state="expanded",
                   )
st.markdown("<h1 style='text-align: center; color: white;'>BizCardX: Extracting Business Card Data with OCR</h1>", unsafe_allow_html=True)
def setting_bg():
    st.markdown(f""" <style>.stApp{{
                background: url("https://c4.wallpaperflare.com/wallpaper/720/309/96/gradient-blurred-minimalism-wallpaper-preview.jpg");
                background-size: cover}}
                </style>""",unsafe_allow_html=True)
setting_bg()

select = option_menu(None,["Home","Upload & Extract","Modify"],
                     icons=["house","cloud-upload","pencil-square"],
                     default_index=0,
                     orientation="horizontal",
                     styles = {"nav-link": {"font-size": "35px", "text-align": "centre", "margin": "0px", "--hover-color": "#6495ED"},
                               "icon": {"font-size": "35px"},
                               "container" : {"max-width": "6000px"},
                               "nav-link-selected": {"background-color": "#6495ED"}})

# MYSQL CONNECTION AND EASY-OCR CALLING
reader = easyocr.Reader(["en"])

myconnection=pymysql.connect(host='127.0.0.1',user='root',password='admin',database="bizcard",port=3306)
cur=myconnection.cursor()

# SQL TABLE CREATION
myconnection=pymysql.connect(host='127.0.0.1',user='root',password='admin',database="bizcard",port=3306)
cur=myconnection.cursor()
cur.execute('''create table if not exists bizcard_data
            (Id int Primary Key AUTO_INCREMENT,
            Company_Name text,
            Card_Holder text,
            Designation text,
            Mobile_Number varchar(50),
            Email text,
            Website text,
            Address text,
            City text,
            State text,
            Pin_Code varchar(20),
            Image longblob)''')
myconnection.commit()

if select == "Home":
    col1,col2=st.columns(2)
    with col1:
        st.markdown("## BizCardx")
        st.subheader("BizCardX: Extracting Business Card Data with OCR")
        st.subheader("Overview of BizCardx")
        st.write('''Application that allows users to upload an image of a business card and extract relevant information from it using
                    easyOCR. The extracted information includes the company name, card holder
                    name, designation, mobile number, email address, website URL, area, city, state,
                    and pin code. The extracted information was displayed in the application's
                    graphical user interface (GUI).
                    ''')
        st.write('''In addition, the application allows users to save the extracted information into
                    a database along with the uploaded business card image. The database can be
                    able to store multiple entries, each with its own business card image and extracted
                    information.
                    ''')
        st.subheader("Approach in this Application")
        st.write("1. Install the required packages mentioned below in Techologies used")
        st.write("2. Design the user interface using streamlit")
        st.write("3. Implement the image processing and OCR for extract the text from image")
        st.write("4. Implement database integration using MySQL or SQLite")
    
        st.markdown("## Technologies Used: ")
        
        st.write("1. Python Scripting")
        st.write("2. Pandas")
        st.write("3. Easy-OCR")
        st.write("4. MySQL")
        st.write("5. Streamlit")
        
        st.write("Project done by VINOTH")
        
    with col2:
        st.image("https://fiverr-res.cloudinary.com/images/t_main1,q_auto,f_auto,q_auto,f_auto/gigs/292442408/original/4826ec125e65902ee6e7e1a2851f85ed6d99e8f1/convert-images-and-rewrite-their-content-into-texts-and-prepare-researches.jpg")
        st.image("https://miro.medium.com/v2/resize:fit:1144/1*7HpOj6xOfAGlKQfYwvAbqA.gif")

if select == "Upload & Extract":
    st.markdown("## Upload a Business Card")
    uploaded_card=st.file_uploader("Upload Here",label_visibility="collapsed",type=["png","jpg","jpeg"])
    
    if uploaded_card is not None:
        
        def card(uploaded_card):
            # # Generate a timestamp to make the filename unique
            # timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            # # Create a directory if it doesn't exist
            # directory = "uploaded_cards"
            # os.makedirs(directory, exist_ok=True)
            # # Construct the dynamic filename using the timestamp
            # filename = f"card_{timestamp}_{uploaded_card.name}"
            # # Join the directory and filename to create the full path
            # full_path = os.path.join(directory, filename)
            # # Write the content of the uploaded card to the file            
            with open(os.path.join("uploaded_cards",uploaded_card.name), "wb") as f:
                f.write(uploaded_card.getbuffer())
        card(uploaded_card)
        
        
        def box_preview(img,text):
            # To Make a RECTANGLE box on text
            for(bbox,text,prob) in text:
                (tl,tr,br,bl)=bbox
                tl = (int(tl[0]), int(tl[1]))
                tr = (int(tr[0]), int(tr[1]))
                br = (int(br[0]), int(br[1]))
                bl = (int(bl[0]), int(bl[1]))
                cv2.rectangle(img, tl,br, (0,255,0), 3)
                cv2.putText(img, text, (tl[0], tl[1] - 10), cv2.FONT_HERSHEY_COMPLEX, 0.65, (255,0,0),2)
            plt.rcParams['figure.figsize']=(15,15)
            plt.axis('off')
            plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
            plt.show()
        
        col1,col2=st.columns(2,gap="large")
        
        with col1:
            st.markdown("#     ")
            st.markdown("#     ")
            st.markdown("### You have uploaded the card")
            st.image(uploaded_card)
            
        with col2:
            st.markdown("#    ")
            st.markdown("#    ")
            with st.spinner("Image Processing and Data Extracting Under Process..."):
                st.set_option('deprecation.showPyplotGlobalUse', False)
                image_path = os.path.join(os.getcwd(), "uploaded_cards", uploaded_card.name)
                img = cv2.imread(image_path)
                text = reader.readtext(image_path)
                st.markdown("### Image Processed and Data Extracted")
                st.pyplot(box_preview(img, text))

            st.success("Processing Completed!")
                
            # image=os.getcwd() + "\\" + "uploaded_cards" + "\\" + uploaded_card.name
            result = reader.readtext(image_path,detail=0,paragraph=False)
        
        def binary(file):
            with open(file, "rb") as file:
                binaryData = file.read()
            return binaryData
        
        data = {"company_name" : [],
                "card_holder" : [],
                "designation" : [],
                "mobile_number" :[],
                "email" : [],
                "website" : [],
                "address" : [],
                "city" : [],
                "state" : [],
                "pin_code" : [],
                "image" : binary(image_path)
               }
        
        def get_data(text):
            for index,i in enumerate(text):
                
                if "www " in i.lower() or "www." in i.lower():
                    data["website"].append(i)
                elif "WWW" in i:
                    data["website"] = text[4] + "." + text[5]
                    
                elif "@" in i:
                    data["email"].append(i)
                    
                elif "-" in i:
                    data["mobile_number"].append(i)
                    if len(data["mobile_number"]) == 2:
                        data["mobile_number"] = "&".join(data["mobile_number"])
                        
                elif  index == 0:
                    data["card_holder"].append(i)
                    
                elif index == 1:
                    data["designation"].append(i)
                    
                elif index == len(text)-1:
                    data["company_name"].append(i)
                    
                if re.findall('^[0-9].+, [a-zA-Z]+',i):
                    data["address"].append(i.split(',')[0])
                elif re.findall('[0-9] [a-zA-Z]+',i):
                    data["address"].append(i)
                    
                match1 = re.findall('.+St , ([a-zA-Z]+).+', i)
                match2 = re.findall('.+St,, ([a-zA-Z]+).+', i)
                match3 = re.findall('^[E].*',i)
                if match1:
                    data["city"].append(match1[0])
                elif match2:
                    data["city"].append(match2[0])
                elif match3:
                    data["city"].append(match3[0])
                    
                
                state_match = re.findall('[a-zA-Z]{9} +[0-9]',i)
                if state_match:
                     data["state"].append(i[:9])
                elif re.findall('^[0-9].+, ([a-zA-Z]+);',i):
                    data["state"].append(i.split()[-1])
                if len(data["state"])== 2:
                    data["state"].pop(0)
                    
                
                if len(i)==6 and i.isdigit():
                    data["pin_code"].append(i)
                elif re.findall('[a-zA-Z]{9} +[0-9]',i):
                    data["pin_code"].append(i[10:])
        get_data(result)
        
        def dataframe(data):
            df=pd.DataFrame(data)
            return df
        df=dataframe(data)
        st.success("### Data Frame Created")
        st.write(df)
        
        if st.button("Upload Data to Database"):
            for i,row in df.iterrows():
                
                cur.execute("SELECT * FROM bizcard_data WHERE card_holder = %s", (data["card_holder"][0],))
                existing_record = cur.fetchone()
                # Eliminating Repeated Records in Data Base
                if existing_record:
                    st.warning("Card holder already exists in the database. Please choose another card.")
                else:
                    # Insert new record into the database
                    query = '''INSERT INTO bizcard_data
                            (company_name, card_holder, designation, mobile_number, email, website, address, city, state, pin_code, image)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
                    cur.execute(query, tuple(row))
                    myconnection.commit()
                    st.success("Uploaded to the database successfully")
            
       
if select == "Modify":
    col1,col2,col3 = st.columns([3,3,2])
    col2.markdown("## Here you can Modify (Alter or Delete the datas)")
    column1,column2 = st.columns(2,gap="large")
    
    try:
        with column1:
            cur.execute("select card_holder from bizcard_data")
            result=cur.fetchall()
            cards_={}
            for row in result:
                cards_[row[0]]=row[0]
            select_card=st.selectbox("Select a card holder name to get datas and update", list(cards_.keys()))
            cur.execute("select company_name,card_holder,designation,mobile_number,email,website,address,city,state,pin_code from bizcard_data where card_holder = %s",
                        (select_card,))
            result=cur.fetchone()
            
            company_name = st.text_input("Company_Name", result[0])
            card_holder = st.text_input("Card_Holder", result[1])
            designation = st.text_input("Designation", result[2])
            mobile_number = st.text_input("Mobile_Number", result[3])
            email = st.text_input("Email", result[4])
            website = st.text_input("Website", result[5])
            address = st.text_input("Address", result[6])
            city = st.text_input("City", result[7])
            state = st.text_input("State", result[8])
            pin_code = st.text_input("Pin_Code", result[9])
            
            if st.button("Commit changes in DataBase"):
                cur.execute("""UPDATE bizcard_data SET company_name=%s,card_holder=%s,designation=%s,mobile_number=%s,email=%s,website=%s,address=%s,city=%s,state=%s,pin_code=%s
                                    WHERE card_holder=%s""", (company_name,card_holder,designation,mobile_number,email,website,address,city,state,pin_code,select_card))
                myconnection.commit()
                st.success("Information updated in database successfully")
        with column2:
            cur.execute("select card_holder from bizcard_data")
            result=cur.fetchall()
            cards_={}
            for row in result:
                cards_[row[0]]=row[0]
            select_card=st.selectbox("Select the card holder name to Delete the datas",list(cards_.keys()))
            st.write(f"### You have selected :red[**{select_card}'s**] card to delete")
            if st.button("Delete Card"):
                cur.execute(f"delete from bizcard_data where card_holder = '{select_card}'")
                myconnection.commit()
                st.success("Card dats deleted from DataBase")
    except:
        st.warning("There is no data available in DataBase")
        
    if st.button("View modified data"):
        cur.execute("select company_name,card_holder,designation,mobile_number,email,website,address,city,state,pin_code from bizcard_data")
        modified_df=pd.DataFrame(cur.fetchall(),columns=["Company_Name","Card_Holder","Designation","Mobile_Number","Email","Website","Address","City","State","Pin_Code"])
        st.write(modified_df)

                