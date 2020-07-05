import ipywidgets as widgets
from IPython.display import display, clear_output
import pandas as pd

def formularz():
    #słownik
    miesiace = [(1, 'January'),(2,'February'),(3,'March'),(4,'April'),(5,'May'),(6,'June'),(7,'July'),(8,'August'),(9,'September'),(10,'October'),(11,'November'),(12,'December')]
    #miesiace = ['January','February','March','April','May','June','July','August','September','October','November','December']
    property = ['Apartment','Bed_Breakfast','Boat','Bungalow','Cabin','Camper_RV','Chalet','Condominium','Dorm','House','Loft','Other','Townhouse','Yurt']
    room = ['Entire_Home_apt','Private_room','Shared_room']
    zip_code = ['98101','98102','98103','98104','98105','98106','98107','98108','98109','98112','98115','98116','98117','98118','98119','98121','98122','98125','98126','98133','98134','98136','98144','98146','98177','98178','98199']
    
    clik_miesiac = widgets.IntSlider(description='Miesiąc:', value=1, min=1, max=12)
    #clik_miesiac = widgets.Dropdown(description='Miesiąc:', options=miesiace)
    #clik_miesiac = widgets.Select(description='Month:', options=miesiace)
    clik_property = widgets.Dropdown(description='Property type:', options=property, layout={'width': 'max-content'})
    #clik_room = widgets.RadioButtons(description='Room type:', options=room)
    clik_room = widgets.ToggleButtons(description='Room type:', options=room)
    clik_guest = widgets.Checkbox(value=False, description='Guest included', disabled=False)
    clik_extra_people = widgets.Checkbox(value=False, description='Extra people', disabled=False)
    clik_cleaning = widgets.Checkbox(value=False, description='Cleanig fee', disabled=False)
    clik_superhost = widgets.Checkbox(value=False, description='Superhost', disabled=False)
    clik_zip_code = widgets.Select(description='Zip code:', options=zip_code, disabled=False)
    clik_bedrooms = widgets.IntSlider(description='Bedrooms:', value=1, min=1, max=5)
    clik_beds = widgets.IntSlider(description='Beds:', value=1, min=1, max=5)
    clik_bathrooms = widgets.IntSlider(description='Bathrooms:', value=1, min=1, max=5)
    
    # ostateczna ramka
    left_box = widgets.VBox([clik_zip_code, clik_miesiac, clik_property, clik_room])
    right_box = widgets.VBox([clik_guest, clik_extra_people, clik_cleaning, clik_superhost, clik_bedrooms, clik_beds, clik_bathrooms])
    box = widgets.HBox([left_box, right_box])
    
    #pokaż
    display(box)
    
def click_button_moj(button_moj):
    #clear_output()  # wyczyszczenie pamiecie - czysci również przycisk
    print(f'Miesiąc: {clik_miesiac.value}, Property type: {clik_property.value}, Room type: {clik_room.value}, \n \
    Guest included: {clik_guest.value}, Extra people: {clik_extra_people.value}, Cleanig fee: {clik_cleaning.value}, \n \
    Superhost: {clik_superhost.value}')
    