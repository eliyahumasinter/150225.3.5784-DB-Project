from random import random, randint, choice
from random_address import real_random_address


IATAs = ["ATL", "LAX", "ORD", "DFW", "DEN", "JFK", "SFO", "SEA", "LAS", "MCO", "EWR", "MIA", "CLT", "PHX", "IAH", "MSP", "BOS", "DTW", "PHL", "LGA", "FLL", "BWI", "SAN", "MDW", "IAD", "DCA", "HNL", "TPA", "PDX", "STL", "SLC", "MCI", "MSY", "CVG", "OAK", "SMF", "RDU", "IND", "SAT", "PIT", "SNA", "CLE", "TLV", "BNA", "AUS", "DAL", "MKE", "BDL", "SJC", "ABQ", "BHM", "BUF", "JAX", "RSW", "OGG", "CMH", "GRR", "TUS", "DAY", "ORF", "GSO", "GSP", "SRQ", "OKC", "ICT", "MEM", "BTV", "LIT", "CHS", "BOI", "HSV", "PBI", "SYR", "AMA", "GRB", "BZN", "FAR", "PVD", "CAK", "EUG", "MHT", "RIC", "PWM", "CID", "LBB", "FAT", "GEG", "ALB", "XNA", "CRP", "GPT", "AVL", "SDF", "ROC", "BTR", "RNO", "LAN", "ELP",
         "MYR", "TYS", "COS", "SAV", "EVV", "ERI", "GNV", "MFR", "BGR", "BMI", "JNU", "FNT", "AGS", "TLH", "SPI", "CHO", "JAN", "LAN", "ERI", "ROA", "SRQ", "LFT", "TOL", "MCN", "OAJ", "LEX", "SBN", "MGM", "AVL", "YVR", "YYZ", "YYC", "YUL", "YEG", "YOW", "YYZ", "YHZ", "YWG", "YXE", "YHM", "YXX", "YLW", "YQR", "YQB", "YXE", "YWG", "YOW", "YHZ", "YXE", "YQG", "YXU", "YKF", "YCD", "YQT", "YXX", "YXX", "YZV", "YXY", "YBR", "YSB", "YQT", "YCG", "YXJ", "YMM", "YXY", "YZP", "YXC", "YQG", "YQU", "YXS", "YTS", "YTH", "YRT", "YUL", "YKF", "YZV", "YQY", "YQB", "YFC", "YCD", "YKA", "YXS", "YBL", "YQG", "YSR", "YDF", "YXU", "YHM", "YXH", "YSB", "YXY", "YQR", "YLL", "YQT", "YTS", "YQY", "YWG", "YMM", "YZF", "YBR"]
luggage_types = ["checked", "carryOn",
                 "personal", "special", "fragile", "equipment"]
medical_field = ['emergencyMedicine', 'travelMedicine', 'occupationalHealth',
                 'publicHealth', 'mentalHealth', 'firstAid', 'airportClinic']

crew_type = ['rampAgent', 'baggageHandler', 'technician', 'fueler',
             'cleaner', 'gse', 'caterer', 'security', 'supervisor', 'tugger']

first_names = ["Tristian","Paityn","Cornelius","Jessie","Wyatt","Molly","Savanna","Hayley","Winston","Rayne","Roland","Sienna","Melvin","Clara","Theodore","Kathleen","Mckenna","Danna","Xzavier","Kamryn","Julissa","Barrett","Lawson","Yareli","Tyrone","Colt","Alvin","Maurice","Camila","Conor","Kirsten","Tatum","Mollie","Todd","Rene","Ismael","Evangeline","Augustus","Kaydence","Emmy","Riya","Simone","Rodney","Kayla","Gaven","Bridget","Cristina","Jenna","Kaelyn","Adalyn","Santino","Noah","Yadira","Julio","Noemi","Kenya","Ainsley","Aisha","Ernest","Yurem","Antonio","Raphael","Haiden","Stephanie","Janet","Luna","Beckham","Carolyn","Layton","Shyla","Arianna","Jordan","Aryanna","Gloria","Gemma","Cash","Edwin","Ann","Angel","Izayah","Maddox","Charlee","Leandro","Gracie","Niko","Nolan","Kale","Carmen","Jaylynn","Alexander","Britney","Lorena","Andrea","Jayson","Ralph","Atticus","Kolton","Karsyn","Arnav","Emelia","Abagail","Mathew","Ishaan","Kyan","Stella","Amiya","Waylon","Trey","Sharon","Brielle","Julie","Giana","Ryan","Bailey","Ayla","Maverick","Alexandra","Brock","Makayla","Lila","Yusuf","Tobias","Malik","Abdiel","Reyna","Kamari","Kayleigh","Giovanni","August","Cohen","Jazmine","Ruby","Crystal","Baylee","Clinton","Callie","Amaris","Casey","Eddie","Donald","Triston","Henry","Emery","Ashton","Skyler","Nathalie","Joe","Keyla","Manuel","Grayson","Isiah","Elisha","Alexa","Alicia","Edgar","Bria","Lilah","Kiera","Richard","Braxton","Marvin","Bryan","Katherine","Rey","Lexie","Gerardo","Jasper","Phoenix","Caylee","Terry","Madyson","Will","Nicole","Louis","Zackary","Jabari","Maci","Frederick","Jackson","Jayden","Kyle","Eva","Eliezer","Kendall","Sawyer","Shaylee","Trevin","Edward","Mohammad","Tommy","Titus","Brodie","Simeon","Rubi","Harmony","Eve","Malachi","Miguel","Zoe","Rowan","Kaylen","Ivy","Zaria","Quintin","Damarion","Kristian","Cristopher","Jenny","Anahi","Lina","Stephany","Kaya","Akira","Lucille","Piper","Seth","Holden","Adriel","Abril","Shyanne","Broderick","Emmanuel","Justine","Selah","Yael","Bryce","Katelyn","Alden","Daphne","Marcelo","Raquel","Landon","Josh","Jaquan","Nathan","Maya","Naomi","Aubrey","Sterling","Makai","Dylan","Rigoberto","Addyson","Cody","Karlee","Rachel","Laylah","Patricia","Roger","Deborah","Mariam","Harry","Dakota","Denzel","Charles","Shania","Jacey","Quincy","Max","Bradyn","Quinton","Braelyn","Imani","Dangelo","Willie","Teresa","Elaine","Carlee","Wayne","Dalton","Alana","Jovani","Cali","Perla","Areli","Ruben","Geovanni","Lea","Kailyn","Branson","Alexzander","Evan","Breanna","Lydia","Bronson","Annie","Aracely","Walker","Elliana","Skyler","Izabella","Kason","Jazlene","Madilynn","Felix","Maxwell","Abigayle","Jaylin","Cheyenne","Case","Lorelei","Humberto","Adrienne","Taniya","Adison","Alejandro","Rhys","Adrianna","Alyvia","Leticia","Ali","Cora","Kenny","Alisha","Mason","Riley","Tania","Mike","Sarahi","Jaylon","Macey","Grant","Ayden","Donna","Bruce","Kamron","Kiersten","Payton","Lilliana","Jakobe","Jamie","Kareem","Jacquelyn","Asia","Madeline","Landen","Ezra","Elias","Haley","Kaitlynn","Roy","Virginia","Joyce","Eli","Danika","Greta","Darryl","Dorian","Lyric","Bella","Carleigh","Talon","Ayanna","Bailee","Lamont","Madilyn","Yosef","Addison","Rihanna","Jayce","Carlie","Bridger","Tucker","Zaid","Alison","Kierra","Bennett","Leonard","Joel","Claire","Gilberto","Allyson","Alisson","Litzy","Chanel","Zaiden","Macie","Mariela","Adyson","Alexis","Donavan","Rex","Scarlett","Ryker","Jonah","Carmelo","Howard","Eric","Angelica","Marina","Nikolas","Jordin","Jaden","Isaias","Yuliana","Katrina","Campbell","Franco","Valerie","Ramiro","Felipe","Ruth","Jaycee","Keely","Kaden","Gracelyn","Halle","Kenzie","Cindy","Israel","Zachery","Conrad","Rowan","Mayra","Natalia","Rory","Marissa","Milton","Ingrid","Leonardo","Frances","Desiree","Aliya","Trevon","Konner","Maryjane","Lincoln","Summer","Alissa","Micaela","Alan","Mackenzie","Cale","Cecelia","Jorge","Landyn","Haylee","Helen","Rachael","Gabriela","Avah","Preston","Lana","Shelby","Gunner","Reese","Gavyn","Mya","Jace","Tabitha","Zaniyah","Matthias","Irvin","Marisa","Amara","Reid","Macy","Ronnie","Nola","Kenneth","Fatima","Graham","Giovani","Braeden","Ross","Kaleb","Melany","Kaeden","Maximo","George","Quinn","Hailey","Maria","Katelynn","Dylan","Karly","Cullen","Makenzie","Jaxson","Arabella","Elle","Mitchell","Tiara","Sara","Naima","Amirah","Nora","Gary","Dale","Alma","Janiyah","Nickolas","Solomon","Neveah","Amelie","Sierra","Malia","Octavio","Hope","Dwayne","Logan","Dominick","Kieran","Bo","Jan","Paige","Sophie","Fabian","Philip","Giselle","Bianca","Phoenix","Kaila","Lindsay","Issac","Hugh","Alina","Nathaniel","Jaqueline","Keith","Davion","Eliana","Myah","Alani","Liana","Declan","Maddison","Billy","Caiden","Nyasia","Savannah","Aylin","Bentley","Jaeden","Tori","Anabella","Alfonso","Erick","Alanna","King","Anika","Albert","Devan","Reynaldo","Boston","Autumn","Presley","Zion","Annabelle","Quinn","Jadyn","Adan","Hazel","Ariel","Sullivan","Samir","Dustin","Trinity","Brody","Misael","Arthur","Raelynn","Isis","Janelle","Adelaide","Frida","Haylie","Malakai","Angeline","Destiny","Elyse","Brenton","Leilani","Shamar","Ashtyn","Maren","Tyrell","Lauren","Gael","Belinda","Lucas","Nathalia","Jett","Ricardo","Jessie","Jadon","Sylvia","Franklin","Trystan","Aria","Derrick","Marques","Mattie","Claudia","Amy","Slade","Ian","Eden","John","Savion","Zachariah","Spencer","Makena","Ben","Kenna","Brent","Lizbeth","Corinne","Hassan","Gideon","Ryleigh","Emmett","Isabell","Rhett","Jaydan","Jennifer","Dana","Marley","Penelope","Dayanara","Charlie","Adam","Sabrina","Josephine","Tony","Lara","Darren","Lilyana","Hanna","Lisa","Emmalee","Libby","Ezequiel","Sloane","Demarcus","Damon","Carly","Wesley","Megan","Kristopher","Agustin","Jeffrey","Nigel","Urijah","Jade","Randy","Anastasia","Kaylie","Keyon","Jesus","Teagan","Dominique","Charlotte","Saniyah","Caitlyn","Aaron","Johanna","Luka","Dario","Emerson","Alex","Charity","Cruz","Roselyn","Chaim","Jocelynn","Lawrence","Kaitlyn","Kylie","Rylee","London","Grace","Sammy","Micheal","Ariella","Weston","Brenna","Kael","Joaquin","Rocco","Leroy","Rylie","Sonny","Trevor","Zoey","Anne","Krystal","Mara","Darian","Houston","Kelsie","Kallie","Justice","Seamus","Aleena","Nikolai","Guadalupe","Susan","Faith","Emilio","Abigail","Nicholas","Aryan","Jamir","Yazmin","Carsen","Jayda","Maximus","Erika","Lilly","Melissa","Aimee","Kyra","Bethany","Van","Journey","Natalya","Marley","Itzel","Ahmad","Camryn","Skye","Catalina","Nathanial","Cassius","Enrique","Yadiel","Antoine","Oscar","Demetrius","Levi","Amani","Zayden","Yesenia","Paul","Giancarlo","Tanner","Yandel","Jean","Payton","Camron","Siena","Luke","Audrey","Brylee","Collin","Brogan","Leyla","Jaida","Delaney","Kristina","Tripp","Aniyah","Cortez","Evelin","Asa","Brycen","Luciana","Memphis","Terrell","April","Kameron","Alyssa","Diana","Ryann","Gianni","Jaslyn","Hillary","Aden","Santos","Jamya","Jordan","Darion","Shirley","Maleah","Deandre","Kiley","Fisher","Hamza","Renee","Brooks","Maribel","Armani","Trenton","Rolando","Aileen","Carlo","Finn","Chace","Aliana","Nataly","Pierre","Leonidas","Kasen","Ernesto","Hayden","Brice","Lee","Mallory","Livia","Rosemary","Ryan","Annika","Kristin","Sonia","Keenan","Valeria","Elian","Darrell","Micah","Joey","Harley","Clay","Alberto","Byron","Moses","Simon","Ashanti","James","Quinten","Vicente","Ashlynn","Kennedi","Eugene","Freddy","Cierra","Marlon","Barbara","Yasmin","Marin","Kamari","Edith","Linda","Emiliano","Vance","Sandra","Stanley","Danica","Everett","Darwin","Beau","Deshawn","Kendall","Chandler","Karli","Lorelai","Madalynn","Eduardo","Noe","Pranav","Colton","Lainey","Oliver","Jazlynn","Cristal","Cedric","Ada","Heidi","Jessica","Mckayla","Nylah","Colten","Maggie","Miriam","Michaela","Krista","Jaiden","Deon","Morgan","Arely","Tessa","Aidan","Andre","Cherish","Darnell","Jayden","Kathy","Cecilia","Samara","Haleigh","Angie","Justice","Braiden","Marcel","Magdalena","Lorenzo","Justus","Serena","Emerson","Hector","Harrison","Dax","Keira","Pedro","Kara","Cael","Krish","Ari","Joselyn","Francis","Dayana","Josiah","Karlie","Kamden","Tamia","Heidy","Abel","Omari","Saul","Juliette","Jared","Reese","Emely","Parker","Clark","Mary","Semaj","Denise","Lamar","Javier","Gordon","Amina","Gabrielle","Mariana","Brendon","Khalil","Elisa","Sadie","Rudy","Amira","Rogelio","Jasmine","Parker","Cordell","Kole","Jair","Mia","Luca","Brynn","River","Jeramiah","Paxton","Christian","Camille","Cason","Josie","Kamren","Bobby","Skylar","Kevin","Brooklynn","Chloe","Rosa","Maliyah","Jordyn","Makhi","Tyree","Danielle","Rebekah","Mckinley","Davian","Karissa","Paloma","Carson","Lilia","Princess","Aydin","Lacey","Jonathan","Timothy","Kaylah","Raiden","Braylen","Leslie","Melina","Marlee","Michael","Giuliana","Ibrahim","Leonel","Liliana","Dashawn","Ronald","Jonathon","Deegan","Alivia","Aydan","Marcos","Matias","Orlando","Calvin","Yasmine","Kasey","Angelique","Lola","Hailie","Karina","Jase","Precious","Sophia"]
last_names = ["Leblanc","Velazquez","Glass","Simpson","Blevins","Gomez","Donovan","Bruce","Richards","Schwartz","Arellano","Gonzales","Chapman","Pena","Cook","Arnold","Lawson","Rodriguez","Blackwell","Stephens","Hughes","Moon","Benjamin","Ayers","Sanchez","Stout","Frye","Carlson","Russell","Mays","Lyons","Wall","Navarro","Perry","Nunez","Carpenter","Higgins","Fitzpatrick","Brady","Frey","Dillon","Sellers","Nash","Aguirre","Warren","Chung","Henson","Byrd","Warner","Burns","Hudson","Bray","Mckinney","Stark","Bowers","Trujillo","Lam","Singleton","Rollins","Osborne","Underwood","Nelson","Barton","Hoffman","Krueger","Leon","Rasmussen","Washington","Maynard","Tyler","Barnett","Sweeney","Dunlap","Cowan","Mendez","Griffith","Lowery","Dickson","Bond","Avila","Clayton","Church","Berry","Rivas","Erickson","Vargas","Peterson","Zimmerman","Sanford","Owen","Carroll","Andrade","Chen","Odom","Wilson","Jefferson","Phillips","Cherry","Foley","Lara","Cohen","Bowman","Werner","Collier","Estrada","Lin","Bentley","Briggs","Potter","Mack","Tran","Boyd","Booker","Mckee","Shaw","Sherman","Sims","Brooks","Henry","Hancock","Haley","Mullen","Guerrero","Francis","Phelps","Odonnell","Powers","Cannon","Burton","Huffman","Strickland","Figueroa","Dyer","Fuller","Brewer","Fowler","Rubio","Moody","Hart","Mcdaniel","Davis","Short","West","Dudley","Oliver","Keith","Ferguson","Shah","Golden","Santos","Vega","Hurst","Cooley","Mendoza","Hanna","Barron","Ibarra","Burch","Stuart","Torres","Hensley","Castillo","Branch","Hendricks","Young","Roth","Santiago","Mccoy","Sawyer","Schultz","Reese","Best","Weaver","Tate","Gross","Mcconnell","Oneill","Blackburn","Schroeder","Mcgrath","Eaton","Harrington","Dalton","Fuentes","Moyer","Cantu","Sharp","Benton","Fields","French","Foster","Barr","Rose","Villa","Avery","Webb","Bell","Weber","Hood","King","Walsh","Cox","Weiss","Duke","Hatfield","Scott","Moses","Murray","Ramsey","Ewing","Hutchinson","Brandt","Humphrey","Crosby","Bradley","Ford","Buck","Henderson","Huber","Morrison","Maxwell","Mcneil","Mayo","Esparza","Ho","Ali","Vaughan","Wiggins","Reed","Alexander","Hale","Grant","Blankenship","Cooke","Cabrera","Neal","Miles","Pearson","Mata","Morris","Parker","Floyd","Gill","Frost","Mcmahon","Salazar","Bryan","Hopkins","Park","Blake","Brown","Holmes","Rice","Watts","Ashley","Carson","Perkins","Waller","Murillo","Tucker","Bishop","Conley","Cortez","Parrish","Stone","Heath","Rosario","Castaneda","Lane","Huang","Riley","Rivers","Day","Rogers","Haas","Stein","Barber","Kirby","Cardenas","Baldwin","Nguyen","Duarte","Chandler","Daniels","Cochran","Pope","Yoder","Bernard","Gallegos","Zavala","Bass","Irwin","Morse","Calhoun","Rush","Vasquez","Tapia","Salas","Yates","Frederick","Kramer","Ross","Mcpherson","Gallagher","Dickerson","Leach","Stafford","Hunter","Johnston","Salinas","Bates","Pace","Horn","Gardner","Anthony","Wu","Barry","Peck","Lawrence","Hooper","Acosta","Richard","Huynh","Walton","Dunn","Kaiser","Chambers","Russo","Wright","Ferrell","Whitehead","Camacho","Noble","Sampson","Reyes","Nielsen","Madden","Molina","Berg","Gibbs","Singh","Baker","Conway","Marsh","Rich","Randall","Hardy","Schmidt","Rocha","Rowe","Christensen","Holt","Stevenson","Mccormick","Bryant","Bradshaw","Morrow","Wyatt","Booth","Pineda","Manning","Shelton","Hamilton","Black","Logan","Haney","Spears","Summers","Hall","House","Boyle","Hodge","Mcbride","Ryan","Lucero","Shepard","Villegas","Orozco","Mcdowell","Graves","Mcgee","Sandoval","Zhang","Jacobson","Gates","Fitzgerald","Frank","Moss","Choi","Wood","Aguilar","Savage","Saunders","Lucas","Rowland","Jimenez","Espinoza","Spencer","Austin","Thomas","Ortiz","Ruiz","Wang","Hawkins","Kelly","Li","Ballard","Reeves","Cummings","Fischer","Matthews","Alvarez","Ayala","Mcdonald","Farrell","Terry","Hodges","Cross","Alvarado","Mahoney","Obrien","Snyder","Morales","Macias","Costa","Campbell","Atkinson","Robles","Ritter","Michael","Crawford","Dawson","Boyer","Adams","Valdez","Ellison","Vazquez","Hernandez","Howell","Lang","Campos","Cline","Huerta","Meadows","Bautista","Marquez","Olsen","Rangel","Richmond","Hubbard","Durham","Gordon","Sosa","Fleming","Greene","Richardson","Stanton","Guzman","Craig","Mcfarland","Wheeler","Butler","Garrison","Hoover","Cunningham","Lynch","Chavez","Norris","Collins","Hess","Wilkinson","Herring","Orr","James","Whitney","Newton","Allen","Beltran","Snow","Bonilla","Mccullough","Jacobs","Hicks","Fritz","Anderson","Doyle","Caldwell","Mcmillan","Clements","Oconnor","Ellis","Mcguire","Bauer","Browning","Oconnell","Bender","Zamora","Palmer","Hunt","Ware","Harvey","Baxter","Montes","Schneider","Reynolds","Ray","Bullock","Harper","Dougherty","Mcclure","Fox","Vincent","Arias","Diaz","Murphy","Larsen","Mclaughlin","Cameron","Fry","Curry","Mosley","Travis","Wolf","Gillespie","Mora","Frazier","Flores","Andrews","Finley","Cole","Vaughn","Roy","Cordova","Swanson","Roach","Pittman","Goodwin","Burnett","Dodson","Patel","Mejia","Daniel","Garcia","Merritt","Jensen","Page","Medina","Wilkins","Marshall","Clarke","Valenzuela","Pugh","Perez","Joseph","Bridges","Hahn","Charles","Pitts","Hendrix","Everett","Horne","Harrison","Patterson","Steele","Padilla","Hays","Chang","Quinn","Hinton","Velasquez","Mercado","Berger","Abbott","Kennedy","Hogan","Stephenson","Rodgers","Waters","Gould","Stanley","Hartman","Ward","Fisher","Jackson","Robertson","Mckenzie","Winters","Wells","Knox","Fletcher","Rhodes","English","Green","Pruitt","Meyers","Sanders","Duncan","Yang","Joyce","Norman","Jennings","Mckay","Woodard","Edwards","Casey","Contreras","Crane","Pierce","Davila","Sheppard","Roman","Harris","Shaffer","Gonzalez","Meyer","Cuevas","Thornton","Webster","Lester","Kline","Acevedo","Armstrong","Bolton","Bennett","Juarez","Pollard","Poole","Grimes","Malone","Ramos","Bird","Gutierrez","Rojas","Melendez","Barajas","Decker","Dixon","Duran","Kane","Goodman","Gentry","Villanueva","Holder","Dorsey","Preston","Montoya","Lynn","Kemp","Sparks","Livingston","Riggs","Jones","Garza","Strong","Delgado","Schaefer","Soto","Novak","Shepherd","Davenport","Melton","Jordan","Banks","Kim","Atkins","Walls","Hill","Mccall","Kent","Bradford","Daugherty","Hardin","Bush","Benson","Lloyd","Howard","Griffin","Flynn","Colon","Montgomery","Miller","Bartlett","Kelley","Giles","Wiley","Welch","Raymond","Beck","Allison","Vang","Herman","Landry","Braun","Sloan","Stevens","Garner","Carr","Pham","Todd","Rios","Knapp","Archer","Farmer","Barrett","Nicholson","Luna","Chan","Price","Houston","Nolan","Lee","Estes","Horton","Burke","Arroyo","Carney","Norton","Delacruz","Beard","Roberts","Prince","Ortega","Williams","May","Flowers","Fernandez","Reilly","Chase","Patrick","Ball","Khan","Burgess","Clay","Petersen","Levy","Wallace","Harrell","Forbes","Graham","Franco","Santana","Gay","Christian","Mitchell","Woodward","Bean","Holloway","Valencia","Shields","Stokes","Cantrell","Osborn","Becker","Harding","Holden","Freeman","Johns","Hebert","Franklin","Calderon","Carrillo","Brock","Wise","Mcclain","Beasley","Baird","Robbins","Douglas","Lutz","Callahan","Parks","Blair","Dennis","Mcknight","Conner","Faulkner","Morgan","Kidd","Farley","Wolfe","Boone","Marks","Pacheco","Drake","Cobb","Hammond","Benitez","Hansen","Lowe","Potts","Bright","Barker","Schmitt","Hanson","Martinez","Glover","Gaines","Watson","Garrett","Galvan","Galloway","Glenn","Hester","Yu","Buckley","Mccarty","Lewis","Simon","Case","Smith","Mercer","White","Wade","Powell","Payne","Walker","Trevino","Willis","Simmons","Koch","Johnson","Mueller","Vance","Hayes","Moore","Haynes","Davidson","Leonard","David","Downs","Mullins","Moran","Ramirez","Adkins","Gilbert","Mathews","Huff","Rosales","Mills","Klein","Parsons","Mcintosh","Castro","Gray","Gamble","Mccarthy","Suarez","Lindsey","Watkins","Romero","Coleman","Shea","Elliott","Whitaker","Guerra","Gibson","Zuniga","Mclean","Long","Keller","Thompson","Key","Donaldson","Duffy","Patton","Olson","Townsend","Moreno","Valentine","Lopez","Herrera","Oneal","Blanchard","Woods","Chaney","Serrano","Nichols","Sutton","Cruz","Cisneros","Mcintyre","Greer","Small","Lambert","Mason","Hurley","Rivera","Combs","Kirk","Carter","Buchanan","Bowen","Munoz","Clark","Jarvis","Brennan","Mooney","Mathis","Riddle","Good","Sexton","Cain","Knight","Paul","Maldonado","Copeland","Solomon","Pratt","Macdonald","Reid","Coffey","Morton","Wagner","Bailey","Tanner","Carey","Silva","Gregory","Curtis","Dominguez","Ingram","Barnes","Wilcox","Maddox","Nixon","Mccann","Randolph","Solis","Cooper","Terrell","Escobar","Liu","Mayer","Wilkerson","Hobbs","Ponce","Le","Andersen","Meza","Hampton","Turner","Williamson","George","Lozano","Newman","Howe","Owens","Walter","Sullivan","Lamb","Conrad","Wong","Hickman","Petty","Holland","Robinson","Velez","Cervantes","Taylor","Friedman","Weeks","Mann","Harmon","Gilmore","Porter","Evans","Roberson","Pennington","Ochoa","Spence","Hines","Barrera","Larson","Villarreal","Love","Walters","Massey","Deleon","Jenkins","Compton","Hull","Davies","Dean","Middleton","Stewart","Shannon","Skinner","Levine","Martin","Kerr","Monroe","Myers","York","Proctor","Hayden","Krause","Peters","Kaufman","Miranda","Little"]


generated_ids = set()


class Person:
    count = 0
    def __init__(self) -> None:
        self.empId = self.count
        self.count += 1
        self.first_name = choice(first_names)
        self.last_name = choice(last_names)
        self.birthdate = f'{randint(1950, 2003)}/{randint(1, 12)}/{randint(1, 28)}'
        self.empDate = f'{randint(1990, 2023)}/{randint(1, 12)}/{randint(1, 28)}'
        self.address = real_random_address()
        self.address = f"{self.address['address1']}, {self.address['city']}, {self.address['state']}, {self.address['postalCode']}"
        self.address = self.address.replace("'", "")    

    @classmethod
    def get_wage(cls, lower, upper):
        return randint(lower, upper)


_luggageID = 0
_carouselID = 0




def random_luggage():
    global _luggageID
    # tag (id) unique integer
    tag = _luggageID
    _luggageID += 1

    # Random weight from 0-100 rounded to 2 decimal places
    weight = round(random()*100, 2)

    # type cargo_type
    cargo_type = choice(luggage_types)

    # "aircraftId" integer
    aircraftId = randint(1, 1000)
    # "carouselId" integer
    carouselId = randint(1, 100)
    sql = f'INSERT INTO luggage ("tag", "weight", "type", "aircraftId", "carouselId") VALUES ({tag}, {weight}, \'{cargo_type}\', {aircraftId}, {carouselId});'
    return sql


def random_carousel():
    global _carouselID
    # Random carouselId
    carousel_id = _carouselID
    _carouselID += 1
    flightID = randint(1000, 9999)
    size = randint(10, 100)
    terminal = randint(1, 10)
    iata = choice(IATAs)
    sql = f'INSERT INTO carousel ("carouselId", "flightId", "size", "terminal", "iata") VALUES ({carousel_id}, {flightID}, {size}, {terminal}, \'{iata}\');'
    return sql


def random_pilot():
    pilot = Person()
    sql = f'INSERT INTO pilot ("empId", "firstName", "lastName", "wage", "dob", "address", "empDate") VALUES ({pilot.empId}, \'{pilot.first_name}\', \'{pilot.last_name}\', {pilot.get_wage(50, 500)}, \'{pilot.birthdate}\', \'{pilot.address}\', \'{pilot.empDate}\');'
    return sql


def random_attendant():
    attendant = Person()
    sql = f'INSERT INTO attendant ("empId", "firstName", "lastName", "wage", "dob", "address", "empDate") VALUES ({attendant.empId}, \'{attendant.first_name}\', \'{attendant.last_name}\', {attendant.get_wage(20, 200)}, \'{attendant.birthdate}\', \'{attendant.address}\', \'{attendant.empDate}\');'
    return sql


def random_medic():
    medic = Person()
    field = choice(medical_field)
    sql = f'INSERT INTO medic ("empId", "firstName", "lastName", "wage", "dob", "address", "empDate", "field") VALUES ({medic.empId}, \'{medic.first_name}\', \'{medic.last_name}\', {medic.get_wage(50, 500)}, \'{medic.birthdate}\', \'{medic.address}\', \'{medic.empDate}\', \'{field}\');'
    return sql


def random_ground_crew():
    crew = Person()
    field = choice(crew_type)
    sql = f'INSERT INTO ground_crew ("empId", "firstName", "lastName", "wage", "dob", "address", "empDate", "type") VALUES ({crew.empId}, \'{crew.first_name}\', \'{crew.last_name}\', {crew.get_wage(80, 800)}, \'{crew.birthdate}\', \'{crew.address}\', \'{crew.empDate}\', \'{field}\');'
    return sql



def buildLuggage():
    with open('init_sql/luggage.sql', 'w') as f:
        for i in range(170_000):
            try:
                f.write(random_luggage() + '\n')
            except:
                i -= 1
                print('error in luggage', i)
    print("Luggage generated successfully")

def buildCarousel():
    with open('init_sql/carousel.sql', 'w') as f:
        for i in range(30_000):
            try:
                f.write(random_carousel() + '\n')
            except:
                i -= 1
                print('error in carousel', i)
    print("Carousel generated successfully")

def buildPilot():
    with open('init_sql/pilot.sql', 'w') as f:
        for i in range(1000):
            try:
                f.write(random_pilot() + '\n')
            except:
                i -= 1
                print('error in pilot', i)
    print("Pilot generated successfully")

def buildAttendant():
    with open('init_sql/attendant.sql', 'w') as f:      
        for i in range(2000):
            try:
                f.write(random_attendant() + '\n')
            except:
                i -= 1
                print('error in attendant', i)
    print("Attendant generated successfully")

def buildMedic():
    with open('init_sql/medic.sql', 'w') as f:
        for i in range(500):
            try:
                f.write(random_medic() + '\n')
            except:
                i -= 1
                print('error in medic', i)
    print("Medic generated successfully")

def buildGroundCrew():
    with open('init_sql/ground_crew.sql', 'w') as f:
        for i in range(2000):
            try:
                f.write(random_ground_crew() + '\n')
            except:
                i -= 1
                print('error in ground_crew', i)
    print("Ground Crew generated successfully")

# buildCarousel()
# buildLuggage()
# buildPilot()
# buildAttendant()
# buildMedic()
buildGroundCrew()
