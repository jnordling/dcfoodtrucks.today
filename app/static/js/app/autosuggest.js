define([
    'jquery', 'typeahead'
], function($) {

    var trucks = [
        "ATIP", "AZN Eats", "Amorini Panini", "Arepa Crew", "Arepa Zone", 
        "Astro Doughnuts & Fried Chicken", "A’ Lo Cubano", "BBQ Bus", 
        "BONMi", "Baba's Big Bite", "Bada Bing", "Balkanik Taste", 
        "Ball or Nothing", "Banh Mi Annie", "Basil Thyme", "Beach Fries", 
        "Beirut Delights", "Bella Vita Italian Wheels", 
        "Best Mexican Burritos and Tortas", "BiBi Ja", "Big Cheese", "Bite 2 Go", 
        "Borinquen Lunch Box", "Brandon's Little Truck", "Bratwurst King", 
        "Brown Bag", "Bubble Tea Licious", "BurGorilla", "CA Slider Company", 
        "Cajunators", "CapMac", "Capital Chicken & Waffles", "Captain Cookie and the Milk Man", 
        "Caribbean Cafe", "Carmen's Italian Ice", "Carnivore BBQ", "Carolina Q", 
        "Cathy's Bistro", "Chatpat", "Chef Alex", "Chef On Wheels", "Chef Seb", 
        "Chez Adilmos", "Chick-fil-A", "Choupi", "Coles Palette", "Corned Beef King", 
        "Crab Cab", "Crave It", "Creme de la Cupcake", "Crepes Parfait", "Crêpe Love", 
        "Cupcake Joy", "Curbside Crabcakes", "Curbside Cupcakes", "Curley's Q", 
        "DC Ballers", "DC Doner", "DC Empanadas", "DC Greek Food", "DC Pollo", 
        "DC Quesadilla & Wraps", "DC Slices", "DC Sliders", "DC Taco Truck", 
        "Dangerous Pies", "Dirty South Deli", "Dolci Gelati", "Dorothy Moon’s Gourmet Burgers", 
        "Doug The Food Dude", "Ducky's Grub", "El Fuego", "Endless Pastabilities", 
        "Far East Taco Grille", "Fasika Ethiopian Cuisine", "Fava Pot", "Federal City Bros", 
        "Feelin' Crabby", "Fire & Rice", "Firemans Cafe", "Food For The Soul", 
        "Food Force One", "Fresh Green", "FroZenYo To Go", "Fusion Confusion", 
        "George's Buffalo Wings", "Go Fish!", "Goode's Mobile Kitchen", 
        "Goodies Frozen Custard & Treats", "Greatest American Hot Dogs", 
        "Green Eggs and Burgers", "Grids Waffles", "Guapo's", "Halal Grill", 
        "Hardy's BBQ", "Healthy Fool", "Henhouse", "Holy Crepes", "Hot People Food", 
        "Hot Wheels", "House Of Falafel", "Hula Girl Truck", "Hungry Heart", 
        "Italian Subs", "Jamaican Mi Crazy", "Jerk Chicken Festival", "Kababji Food Truck", 
        "Kabob Bites", "Kabob King", "Kabob Palace", "Kafta Mania", "Kalaveras", 
        "Kimchi BBQ Taco", "Korean BBQ Taco Box", "Korengy", "Kraving Kabob", 
        "Kushi-Moto", "LA Taco Truck", "La Tingeria", "Latin & American Flavors", 
        "Lemongrass Truck", "Lilypad On The Run", "Lime Tree", "Linda's Luncheonette", 
        "Little Italy On Wheels", "Little Piece of Heaven", "Los Lobos Burritos", 
        "Mac Attack", "Mac's Donuts", "Mama's Donut Bites", "Mayur Kabob House", 
        "Mediterranean Delight", "Meggrolls", "Melted", "Meski Healthy 2 Go", 
        "Mesob On Wheels", "Miami Vice Burgers", "Midnite Confections Cupcakery", 
        "Mighty Dog And Acai", "Moh Moh Dumpling", "Mojaita Latin Flavor", "MojoTruck", 
        "Mr Miyagi’s Teriyaki", "Naan Stop DC", "NeatMeat", "New York Deli", 
        "Olivia's Cupcakes", "OoH DaT ChickeN", "Orange Cow", "Over the Rice", 
        "Pars Kabob", "Pepe", "Peruvian Brothers", "Phillies Phamous Cheesesteaks", 
        "Pho Junkies", "Pho-Bachi", "PhoWheels", "Phonation", "Pleasant Pops", 
        "Popped! Republic", "Puddin'", "Quick Wraps", "Randy Radish", "Reba's Funnel Cake", 
        "Red Hook Lobster Pound", "Redbone", "Reggae Vibes", "Rio Churrasco", 
        "Rito Loco", "Roaming Rotisserie", "RockSalt", "Rocklands BBQ", "Rollin' Kabob", 
        "Rolls On Rolls", "Roving Italian", "Royal Chicken & Gyro", "SOL Mexican Grill", 
        "SUNdeVICH", "SUSHIPAO", "Saffron Food Lovers", "Sang On Wheels", 
        "Saran's Vegetarian", "Sate", "Scoops2u", "Seoul Food", "Señor Taco", 
        "Sidewalk Sweets", "Simple on Wheels", "Simply Delightful", "Sinplicity Ice Cream", 
        "Sloppy Mama's", "Smokin' On The Bayou", "Smoking Kow BBQ", "South Meets East", 
        "Souvlaki Stop", "Spitfire", "Steak Bites", "Stella’s Popkern", "Street Cream", 
        "Surfside", "SweetArt", "Sweetbites mobile café", "Swizzler", 
        "TSR Quesadillas & Baked Empanadas", "Takorean", "Tapas Truck", 
        "Tasha’s Cookies and Treats", "Taste Of Eastern Europe", "Tasty Fried DC", 
        "Tasty Kabob", "Tasty Toranj", "Thai Machine", "That Cheesecake Truck!", 
        "The Corn Factory", "The Frosted Muffin", "The Wagon", "Tin Heaven", 
        "Tokyo In The City", "Top Dog", "Tops American Food Company", "Tortuga", 
        "Turkish Kabob", "Urban Bumpkin", "Village Cafe Express", "Wassub", "What The Pho?", 
        "Woodland’s Vegan Bistro", "Yella Food", "Yellow Vendor", "Yumm Yum Food", 
        "Yumpling", "Z-Burger Mobile", "Zesty Kabob"
    ];


    var substringMatcher = function(strs) {
        return function findMatches(q, cb) {
            var matches, substringRegex;

            matches = [];

            substrRegex = new RegExp(q, 'i');

            $.each(strs, function(i, str) {
                if (substrRegex.test(str)) {
                    matches.push(str);
                }
            });

            cb(matches);
        };
    };


    $('.typeahead').typeahead({
        hint: true,
        highlight: true,
        minLength: 1
    }, {
        name: 'trucks',
        source: substringMatcher(trucks)
    });



    // handle input submission

    $('.typeahead').keyup(function(e) {
        // enter key press
        if (e.keyCode === 13) {
            do_something($(this).val());
        }
    });


    $('.typeahead').bind('typeahead:select', function(e, val) {
        do_something(val);
    });


    function do_something(txt) {
        console.log('do something with... ' + txt);
        $('.typeahead').blur();
    }


});
