import json
from summary_lambda import handler

event = {
    "body": json.dumps(
        {
            "text": """
            Professional wrestling began in the 19th century as legitimate grappling contests showcased in carnivals and traveling fairs, where athletic competition blended with theatrical flair to captivate audiences. Over time, promoters realized that predetermined outcomes allowed for stronger storytelling, recurring heroes and villains, and more consistent ticket sales. By the mid-20th century, the American wrestling landscape was organized into regional “territories” under the National Wrestling Alliance (NWA), which coordinated champions across different promotions. 
            In the Northeast, Capitol Wrestling Corporation split from the NWA in 1963 to form the World Wide Wrestling Federation (WWWF), later renamed the World Wrestling Federation (WWF). The company thrived on charismatic champions like Bruno Sammartino and built a stronghold at Madison Square Garden.
            The true transformation came in the 1980s when Vince McMahon expanded the WWF nationally, breaking the territorial system. By leveraging cable television and pay-per-view, he turned wrestling into mainstream entertainment. The first WrestleMania in 1985, headlined by stars such as Hulk Hogan, combined celebrity culture with wrestling spectacle and launched a boom period known as the “Rock ’n’ Wrestling” era. 
            In the 1990s, fierce competition from World Championship Wrestling (WCW) sparked the “Monday Night Wars,” pushing the WWF to adopt a more rebellious tone during the Attitude Era. Antiheroes like Stone Cold Steve Austin and The Rock drew massive television audiences and reshaped the company’s identity.
            After acquiring WCW in 2001, the WWF rebranded in 2002 as World Wrestling Entertainment (WWE), reflecting a broader entertainment focus. The 2000s and 2010s saw WWE expand globally, refine its brand split between Raw and SmackDown, and build new icons such as John Cena. The company embraced digital distribution with the WWE Network and later streaming partnerships, adapting to changing media habits. Meanwhile, the women’s division evolved from a secondary attraction to a main-event force, marking a significant cultural shift within the industry. 
            Today, WWE stands as the dominant global wrestling promotion, blending athleticism, storytelling, and multimedia production in a form that continues to evolve while honoring its theatrical roots.
        """
        }
    ),
    "queryStringParameters": {
        "points": "3"
    }
}

response = handler(event, {})

print((json.loads(response["body"]).get("summary")))