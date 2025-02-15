import asyncio
import os
import re
from typing import List

from dotenv import load_dotenv
from anthropic import AsyncAnthropic

load_dotenv()
client = AsyncAnthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

async def get_completion(
    prompt: str,
    model: str="claude-3-5-haiku-latest",
    max_tokens: int=1024,
    temperature: float=0.5,
    system: str="",
    prefill: str="",
    stop_sequences: List[str] = []
):
    async with client.messages.stream(
        model=model,
        max_tokens=max_tokens,
        temperature=temperature,
        system=system,
        messages=[{"role": "user", "content": prompt}, {"role": "assistant", "content": prefill}],
        stop_sequences=stop_sequences
    ) as stream:
        msg = await stream.get_final_message()

        resp = prefill + msg.content[0].text
        if msg.stop_sequence is not None:
            resp += msg.stop_sequence

        return resp

async def exercise_1_1():
    def grade(text):
        pattern = re.compile(r'^(?=.*1)(?=.*2)(?=.*3).*$', re.DOTALL)
        return bool(pattern.match(text))

    resp = await get_completion("Just count to three as number.")
    print(f"Exercise 1.1 has been correctly solved {grade(resp)}: {resp}")

async def exercise_1_2():
    def grade(text):
        text = text.lower()
        return bool(re.search(r"giggles", text) or re.search(r"soo", text))

    PROMPT = "How big is the sky?"
    resp = await get_completion(PROMPT, system="You are a 3 year old child.")
    print(f"Exercise 1.2 has been correctly solved {grade(resp)}: {resp}")

async def exercise_2_1():
    def grade(text):
        return "hola" in text.lower()

    PROMPT = "Hello Claude, how are you?"
    resp = await get_completion(PROMPT, system="Response into spanish")
    print(f"Exercise 2.1 has been correctly solved {grade(resp)}: {resp}")

async def exercise_2_2():
    def grade(text):
        return text == "Michael Jackson"

    resp = await get_completion("Who is the King of Pop? Please answer me just name without any information.")
    print(f"Exercise 2.2 has been correctly solved {grade(resp)}: {resp}")

async def exercise_2_3():
    def grade(text):
        trimmed = text.strip()
        words = len(trimmed.split())
        return words >= 800

    resp = await get_completion("Write a looooong story about a hacker. The story should be longer than 1000 words.", temperature=1.0, max_tokens=4096)
    trimmed = resp.strip()
    words = len(trimmed.split())
    print(f"Exercise 2.3 has been correctly solved {grade(resp)} ({words})")

async def exercise_3_1():
    def grade(text):
        if "incorrect" in text or "not correct" in text.lower():
            return True
        else:
            return False

    PROMPT="""Is this equation solved correctly below?

2x - 3 = 9
2x = 6
x = 3"""

    resp = await get_completion(PROMPT, system="You are a homework checker. So, your answer is must be 'correct' or 'not correct'.", temperature=0.0)
    print(f"Exercise 3.1 has been correctly solved {grade(resp)}: {resp}")

async def exercise_4_1():
    def grade(text):
        return bool(re.search("pigs", text.lower()) and re.search("haiku", text.lower()))

    TOPIC = "Pigs"
    resp = await get_completion(f"Generate haiku about <topic>{TOPIC}</topic>. Haiku must be contains the topic and 'haiku'.")
    print(f"Exercise 4.1 has been correctly solved {grade(resp)}: {resp}")

async def exercise_4_2():
    def grade(text):
        return bool(re.search("brown", text.lower()))

    QUESTION = "ar cn brown?"
    PROMPT = f"Hia its me i have a q about dogs jkaerjv <question>{QUESTION}</question> jklmvca tx it help me muhch much atx fst fst answer short short tx"
    resp = await get_completion(PROMPT)
    print(f"Exercise 4.2 has been correctly solved {grade(resp)}: {resp}")

async def exercise_4_3():
    def grade(text):
        return bool(re.search("brown", text.lower()))

    QUESTION = "ar cn brown?"
    PROMPT = f"Hia its me i have a q about dogs {QUESTION} tx it help me muhch much atx fst fst answer short short tx"
    resp = await get_completion(PROMPT)
    print(f"Exercise 4.3 has been correctly solved {grade(resp)}: {resp}")

async def exercise_5_1():
    def grade(text):
        return bool(re.search("Warrior", text))

    PROMPT = "Who is the best basketball player of all time? Please choose one specific player."
    PREFILL = "Golden" # Golden State Warriors
    resp = await get_completion(PROMPT, prefill=PREFILL)
    print(f"Exercise 5.1 has been correctly solved {grade(resp)}: {resp}")

async def exercise_5_2():
    def grade(text):
        return bool(
            (re.search("cat", text.lower()) and re.search("<haiku>", text))
            and (text.count("\n") + 1) > 5
        )

    ANIMAL = "cats"
    PROMPT = f"Please write 2 haikus about {ANIMAL}. Each haiku put it in <haiku> tags. Each haiku should be clearly distinct from the others. At least one haiku shoulde be contains 'cat'."
    PREFILL = "<haiku>"
    resp = await get_completion(PROMPT, prefill=PREFILL)
    print(f"Exercise 5.2 has been correctly solved {grade(resp)}: {resp}")

async def exercise_5_3():
    def grade(text):
        return bool(re.search("tail", text.lower()) and re.search("cat", text.lower()) and re.search("<haiku>", text))

    ANIMAL1 = "Cat"
    ANIMAL2 = "Dog"
    PROMPT = f"Please write a haiku about {ANIMAL1} and {ANIMAL2}. Each haiku should be put it in <haiku> tags. At least one haiku shoulde be contains 'tail'."
    resp = await get_completion(PROMPT)
    print(f"Exercise 5.3 has been correctly solved {grade(resp)}: {resp}")

async def exercise_6_1():
    PROMPT = """Please classify this email: <email>{email}</email>.

The answer should be one of the following:
(A) Pre-sale question
(B) Broken or defective item
(C) Billing question
(D) Other (please explain)

Your anwser needs to include the letter (A-D) with the parentheses, as well as the name of the category.

Put it in <classification> tag.
"""
    PREFILL="<classification>"
    EMAILS = [
        "Hi -- My Mixmaster4000 is producing a strange noise when I operate it. It also smells a bit smoky and plasticky, like burning electronics.  I need a replacement.", # (B) Broken or defective item
        "Can I use my Mixmaster 4000 to mix paint, or is it only meant for mixing food?", # (A) Pre-sale question OR (D) Other (please explain)
        "I HAVE BEEN WAITING 4 MONTHS FOR MY MONTHLY CHARGES TO END AFTER CANCELLING!!  WTF IS GOING ON???", # (C) Billing question
        "How did I get here I am not good with computer.  Halp." # (D) Other (please explain)
    ]
    ANSWERS = [
        ["B"],
        ["A","D"],
        ["C"],
        ["D"]
    ]
    REGEX_CATEGORIES = {
        "A": "A\\) P",
        "B": "B\\) B",
        "C": "C\\) B",
        "D": "D\\) O"
    }

    for i, email in enumerate(EMAILS):
        formatted_prompt = PROMPT.format(email=email)
        response = await get_completion(formatted_prompt, prefill=PREFILL)
        grade = any([bool(re.search(REGEX_CATEGORIES[ans], response)) for ans in ANSWERS[i]])
        print(f"Exercise 6.1 has been correctly solved {grade}: {response}")

async def exercise_6_2():
    PROMPT = """Please classify this email: <email>{email}</email>.

The answer should be one of the following:
(A) Pre-sale question
(B) Broken or defective item
(C) Billing question
(D) Other (please explain)

Your anwser is just the letter (A-D) without the parentheses.

Put it in <answer> tag.
"""
    PREFILL = "<answer>"
    EMAILS = [
        "Hi -- My Mixmaster4000 is producing a strange noise when I operate it. It also smells a bit smoky and plasticky, like burning electronics.  I need a replacement.", # (B) Broken or defective item
        "Can I use my Mixmaster 4000 to mix paint, or is it only meant for mixing food?", # (A) Pre-sale question OR (D) Other (please explain)
        "I HAVE BEEN WAITING 4 MONTHS FOR MY MONTHLY CHARGES TO END AFTER CANCELLING!!  WTF IS GOING ON???", # (C) Billing question
        "How did I get here I am not good with computer.  Halp." # (D) Other (please explain)
    ]
    ANSWERS = [
        ["B"],
        ["A","D"],
        ["C"],
        ["D"]
    ]
    REGEX_CATEGORIES = {
        "A": "<answer>A</answer>",
        "B": "<answer>B</answer>",
        "C": "<answer>C</answer>",
        "D": "<answer>D</answer>"
    }

    for i, email in enumerate(EMAILS):
        formatted_prompt = PROMPT.format(email=email)
        response = await get_completion(formatted_prompt, prefill=PREFILL)
        grade = any([bool(re.search(REGEX_CATEGORIES[ans], response)) for ans in ANSWERS[i]])
        print(f"Exercise 6.2 has been correctly solved {grade}: {response}")

async def exercise_7_1():
    PROMPT = """Please classify email.

The answer should be one of the following:
(A) Pre-sale question
(B) Broken or defective item
(C) Billing question
(D) Other

Q) <email>I can't typo korean. HELP</email>
A) The correct answer is D

Q) <email>How to cancel my subscription?</email>
A) The correct answer is C

Q) <email>{email}</email>.
"""
    PREFILL = "A) The correct answer is"
    EMAILS = [
        "Hi -- My Mixmaster4000 is producing a strange noise when I operate it. It also smells a bit smoky and plasticky, like burning electronics.  I need a replacement.", # (B) Broken or defective item
        "Can I use my Mixmaster 4000 to mix paint, or is it only meant for mixing food?", # (A) Pre-sale question OR (D) Other (please explain)
        "I HAVE BEEN WAITING 4 MONTHS FOR MY MONTHLY CHARGES TO END AFTER CANCELLING!!  WTF IS GOING ON???", # (C) Billing question
        "How did I get here I am not good with computer.  Halp." # (D) Other (please explain)
    ]
    ANSWERS = [
        ["B"],
        ["A","D"],
        ["C"],
        ["D"]
    ]
    STOP_SEQUENCES = [
        "A",
        "B",
        "C",
        "D",
    ]

    for i, email in enumerate(EMAILS):
        formatted_prompt = PROMPT.format(email=email)
        response = await get_completion(formatted_prompt, prefill=PREFILL, stop_sequences=STOP_SEQUENCES)
        grade = any([bool(re.search(ans, response[-1])) for ans in ANSWERS[i]])
        print(f"Exercise 7.1 has been correctly solved {grade}: {response}")

async def exercise_8_1():
    def grade(text):
        contains = bool(
            re.search("Unfortunately", text) or
            re.search("I apologize", text) or
            re.search("I do not", text) or
            re.search("I don't", text)
        )
        does_not_contain = not bool(re.search("2022", text))
        return contains and does_not_contain

    PROMPT = "In what year did star performer Beyoncé release her eighth studio album? Only answer you know the answer with certainty."
    resp = await get_completion(PROMPT)
    print(f"Exercise 8.1 has been correctly solved {grade(resp)}: {resp}")

async def exercise_8_2():
    def grade(text):
        return bool(re.search("49-fold", text))

    PROMPT = """<question>From December 2018 to December 2022, by what amount did Matterport's subscribers grow?</question>
Please read the below document. Then, in <scratchpad> tags, pull the most relevent quote from the document and consider whether it answers the user's question or whether it lacks sufficient detail. Then write a brief numerical answer in <answer> tags.

<document>
Matterport SEC filing 10-K 2023
Item 1. Business
Our Company
Matterport is leading the digitization and datafication of the built world. We believe the digital transformation of the built world will fundamentally change the way people interact with buildings and the physical spaces around them.
Since its founding in 2011, Matterport’s pioneering technology has set the standard for digitizing, accessing and managing buildings, spaces and places online. Our platform’s innovative software, spatial data-driven data science, and 3D capture technology have broken down the barriers that have kept the largest asset class in the world, buildings and physical spaces, offline and underutilized for many years. We believe the digitization and datafication of the built world will continue to unlock significant operational efficiencies and property values, and that Matterport is the platform to lead this enormous global transformation.
The world is rapidly moving from offline to online. Digital transformation has made a powerful and lasting impact across every business and industry today. According to International Data Corporation, or IDC, over $6.8 trillion of direct investments will be made on digital transformation from 2020 to 2023, the global digital transformation spending is forecasted to reach $3.4 trillion in 2026 with a five-year compound annual growth rate (“CAGR”) of 16.3%, and digital twin investments are expected to have a five-year CAGR of 35.2%. With this secular shift, there is also growing demand for the built world to transition from physical to digital. Nevertheless, the vast majority of buildings and spaces remain offline and undigitized. The global building stock, estimated by Savills to be $327 trillion in total property value as of 2021, remains largely offline today, and we estimate that less than 0.1% is penetrated by digital transformation.
Matterport was among the first to recognize the increasing need for digitization of the built world and the power of spatial data, the unique details underlying buildings and spaces, in facilitating the understanding of buildings and spaces. In the past, technology advanced physical road maps to the data-rich, digital maps and location services we all rely on today. Matterport now digitizes buildings, creating a data-rich environment to vastly increase our understanding and the full potential of each and every space we capture. Just as we can instantly, at the touch of a button, learn the fastest route from one city to another or locate the nearest coffee shops, Matterport’s spatial data for buildings unlocks a rich set of insights and learnings about properties and spaces worldwide. In addition, just as the geo-spatial mapping platforms of today have opened their mapping data to industry to create new business models such as ridesharing, e-commerce, food delivery marketplaces, and even short-term rental and home sharing, open access to Matterport’s structured spatial data is enabling new opportunities and business models for hospitality, facilities management, insurance, construction, real estate and retail, among others.
We believe the total addressable market opportunity for digitizing the built world is over $240 billion, and could be as high as $1 trillion as the market matures at scale. This is based on our analysis, modeling and understanding of the global building stock of over 4 billion properties and 20 billion spaces in the world today. With the help of artificial intelligence (“AI”), machine learning (“ML”) and deep learning (“DL”) technologies, we believe that, with the additional monetization opportunities from powerful spatial data-driven property insights and analytics, the total addressable market for the digitization and datafication of the built world will reach more than $1 trillion.

Our spatial data platform and capture of digital twins deliver value across a diverse set of industries and use cases. Large retailers can manage thousands of store locations remotely, real estate agencies can provide virtual open houses for hundreds of properties and thousands of visitors at the same time, property developers can monitor the entirety of the construction process with greater detail and speed, and insurance companies can more precisely document and evaluate claims and underwriting assessments with efficiency and precision. Matterport delivers the critical digital experience, tools and information that matter to our subscribers about properties of virtually any size, shape, and location worldwide.
For nearly a decade, we have been growing our spatial data platform and expanding our capabilities in order to create the most detailed, accurate, and data-rich digital twins available. Moreover, our 3D reconstruction process is fully automated, allowing our solution to scale with equal precision to millions of buildings and spaces of any type, shape, and size in the world. The universal applicability of our service provides Matterport significant scale and reach across diverse verticals and any geography. As of December 31, 2022, our subscriber base had grown approximately 39% to over 701,000 subscribers from 503,000 subscribers as of December 31, 2021, with our digital twins reaching more than 170 countries. We have digitized more than 28 billion square feet of space across multiple industries, representing significant scale and growth over the rest of the market.

As we continue to transform buildings into data worldwide, we are extending our spatial data platform to further transform property planning, development, management and intelligence for our subscribers across industries to become the de facto building and business intelligence engine for the built world. We believe the demand for spatial data and resulting insights for enterprises, businesses and institutions across industries, including real estate, architecture, engineering and construction (“AEC”), retail, insurance and government, will continue to grow rapidly.
We believe digitization and datafication represent a tremendous greenfield opportunity for growth across this massive category and asset class. From the early stages of design and development to marketing, operations, insurance and building repair and maintenance, our platform’s software and technology provide subscribers critical tools and insights to drive cost savings, increase revenues and optimally manage their buildings and spaces. We believe that hundreds of billions of dollars in unrealized utilization and operating efficiencies in the built world can be unlocked through the power of our spatial data platform. Our platform and data solutions have universal applicability across industries and building categories, giving Matterport a significant advantage as we can address the entirety of this large market opportunity and increase the value of what we believe to be the largest asset class in the world.
With a demonstrated track record of delivering value to our subscribers, our offerings include software subscription, data licensing, services and product hardware. As of December 31, 2022, our subscriber base included over 24% of Fortune 1000 companies, with less than 10% of our total revenue generated from our top 10 subscribers. We expect more than 80% of our revenue to come from our software subscription and data license solutions by 2025. Our innovative 3D capture products, the Pro2 and Pro3 Cameras, have played an integral part in shaping the 3D building and property visualization ecosystem. The Pro2 and Pro3 Cameras have driven adoption of our solutions and have generated the unique high-quality and scaled data set that has enabled Cortex, our proprietary AI software engine, to become the pioneering engine for digital twin creation. With this data advantage initially spurred by the Pro2 Camera, we have developed a capture device agnostic platform that scales and can generate new building and property insights for our subscribers across industries and geographies.
We have recently experienced rapid growth. Our subscribers have grown approximately 49-fold from December 31, 2018 to December 31, 2022. Our revenue increased by approximately 22% to $136.1 million for the year ended December 31, 2022, from approximately $111.2 million for the year ended December 31, 2021. Our gross profit decreased by $8.1 million or 14%, to $51.8 million for the year ended December 31, 2022, from $60.0 million for the year ended December 31, 2021, primarily attributable to certain disruptive and incremental costs due to the global supply chain constraints in fiscal year 2022. Our ability to retain and grow the subscription revenue generated by our existing subscribers is an important measure of the health of our business and our future growth prospects. We track our performance in this area by measuring our net dollar expansion rate from the same set of customers across comparable periods. Our net dollar expansion rate of 103% for the three months ended December 31, 2022 demonstrates the stickiness and growth potential of our platform.
Our Industry and Market Opportunity
Today, the vast majority of buildings and spaces remain undigitized. We estimate our current serviceable addressable market includes approximately 1.3 billion spaces worldwide, primarily from the real estate and travel and hospitality sectors. With approximately 9.2 million spaces under management as of December 31, 2022, we are continuing to penetrate the global building stock and expand our footprint across various end markets, including residential and commercial real estate, facilities management, retail, AEC, insurance and repair, and travel and hospitality. We estimate our total addressable market to be more than 4 billion buildings and 20 billion spaces globally, yielding a more than $240 billion market opportunity. We believe that as Matterport’s unique spatial data library and property data services continue to grow, this opportunity could increase to more than $1 trillion based on the size of the building stock and the untapped value creation available to buildings worldwide. The constraints created by the COVID-19 pandemic have only reinforced and accelerated the importance of our scaled 3D capture solution that we have developed for diverse industries and markets over the past decade.

Our Spatial Data Platform
Overview
Our technology platform uses spatial data collected from a wide variety of digital capture devices to transform physical buildings and spaces into dimensionally accurate, photorealistic digital twins that provide our subscribers access to previously unavailable building information and insights.
As a first mover in this massive market for nearly a decade, we have developed and scaled our industry-leading 3D reconstruction technology powered by Cortex, our proprietary AI-driven software engine that uses machine learning to recreate a photorealistic, 3D virtual representation of an entire building structure, including contents, equipment and furnishings. The finished product is a detailed and dynamic replication of the physical space that can be explored, analyzed and customized from a web browser on any device, including smartphones. The power to manage even large-scale commercial buildings is in the palm of each subscriber’s hands, made possible by our advanced technology and breakthrough innovations across our entire spatial data technology stack.
Key elements of our spatial data platform include:
•Bringing offline buildings online. Traditionally, our customers needed to conduct in-person site visits to understand and assess their buildings and spaces. While photographs and floor plans can be helpful, these forms of two-dimensional (“2D”) representation have limited information and tend to be static and rigid, and thus lack the interactive element critical to a holistic understanding of each building and space. With the AI-powered capabilities of Cortex, our proprietary AI software, representation of physical objects is no longer confined to static 2D images and physical visits can be eliminated. Cortex helps to move the buildings and spaces from offline to online and makes them accessible to our customers in real-time and on demand from anywhere. After subscribers scan their buildings, our visualization algorithms accurately infer spatial positions and depths from flat, 2D imagery captured through the scans and transform them into high- fidelity and precise digital twin models. This creates a fully automated image processing pipeline to ensure that each digital twin is of professional grade image quality.
•Driven by spatial data. We are a data-driven company. Each incremental capture of a space grows the richness and depth of our spatial data library. Spatial data represents the unique and idiosyncratic details that underlie and compose the buildings and spaces in the human- made environment. Cortex uses the breadth of the billions of data points we have accumulated over the years to improve the 3D accuracy of our digital twins. We help our subscribers pinpoint the height, location and other characteristics of objects in their digital twin. Our sophisticated algorithms also deliver significant commercial value to our subscribers by generating data-based insights that allow them to confidently make assessments and decisions about their properties. For instance, property developers can assess the amount of natural heat and daylight coming from specific windows, retailers can ensure each store layout is up to the same level of code and brand requirements, and factories can insure machinery layouts meet specifications and location guidelines. With approximately 9.2 million spaces under management as of December 31, 2022, our spatial data library is the clearinghouse for information about the built world.
•Powered by AI and ML. Artificial intelligence and machine learning technologies effectively utilize spatial data to create a robust virtual experience that is dynamic, realistic, interactive, informative and permits multiple viewing angles. AI and ML also make costly cameras unnecessary for everyday scans—subscribers can now scan their spaces by simply tapping a button on their smartphones. As a result, Matterport is a device agnostic platform, helping us more rapidly scale and drive towards our mission of digitizing and indexing the built world.
Our value proposition to subscribers is designed to serve the entirety of the digital building lifecycle, from design and build to maintenance and operations, promotion, sale, lease, insure, repair, restore, secure and finance. As a result, we believe we are uniquely positioned to grow our revenue with our subscribers as we help them to discover opportunities to drive short- and long-term return on investment by taking their buildings and spaces from offline to online across their portfolios of properties.
Ubiquitous Capture
Matterport has become the standard for 3D space capture. Our technology platform empowers subscribers worldwide to quickly, easily and accurately digitize, customize and manage interactive and dimensionally accurate digital twins of their buildings and spaces.
The Matterport platform is designed to work with a wide range of LiDAR, spherical, 3D and 360 cameras, as well as smartphones, to suit the capture needs of all of our subscribers. This provides the flexibility to capture a space of any size, scale, and complexity, at anytime and anywhere.
•Matterport Pro3 is our newest 3D camera that scans properties faster than earlier versions to help accelerate project completion. Pro3 provides the highest accuracy scans of both indoor and outdoor spaces and is designed for speed, fidelity, versatility and accuracy. Capturing 3D data up to 100 meters away at less than 20 seconds per sweep, Pro3’s ultra-fast, high-precision LiDAR sensor can run for hours and takes millions of measurements in any conditions.
•Matterport Pro2 is our proprietary 3D camera that has been used to capture millions of spaces around the world with a high degree of fidelity, precision, speed and simplicity. Capable of capturing buildings more than 500,000 square feet in size, it has become the camera of choice for many residential, commercial, industrial and large-scale properties.
•360 Cameras. Matterport supports a selection of 360 cameras available in the market. These affordable, pocket sized devices deliver precision captures with high fidelity and are appropriate for capturing smaller homes, condos, short-term rentals, apartments, and more. The spherical lens image capture technology of these devices gives Cortex robust, detailed image data to transform panoramas into our industry-leading digital twins.
•LEICA BLK360. Through our partnership with Leica, our 3D reconstruction technology and our AI powered software engine, Cortex, transform this powerful LiDAR camera into an ultra-precise capture device for creating Matterport digital twins. It is the solution of choice for AEC professionals when exacting precision is required.
•Smartphone Capture. Our capture apps are commercially available for both iOS and Android. Matterport’s smartphone capture solution has democratized 3D capture, making it easy and accessible for anyone to digitize buildings and spaces with a recent iPhone device since the initial introduction of Matterport for iPhone in May 2020. In April 2021, we announced the official release of the Android Capture app, giving Android users the ability to quickly and easily capture buildings and spaces in immersive 3D. In February 2022, we launched Matterport Axis, a motorized mount that holds a smartphone and can be used with the Matterport Capture app to capture 3D digital twins of any physical space with increased speed, precision, and consistency.
Cortex and 3D Reconstruction (the Matterport Digital Twin)
With a spatial data library, as of December 31, 2022, of approximately 9.2 million spaces under management, representing approximately 28 billion captured square feet of space, we use our advanced ML and DL technologies to algorithmically transform the spatial data we capture into an accurate 3D digital reproduction of any physical space. This intelligent, automated 3D reconstruction is made possible by Cortex, our AI-powered software engine that includes a deep learning neural network that uses our spatial data library to understand how a building or space is divided into floors and rooms, where the doorways and openings are located, and what types of rooms are present, such that those forms are compiled and aligned with dimensional accuracy into a dynamic, photorealistic digital twin. Other components of Cortex include AI-powered computer vision technologies to identify and classify the contents inside a building or space, and object recognition technologies to identify and segment everything from furnishings and equipment to doors, windows, light fixtures, fire suppression sprinklers and fire escapes. Our highly scalable artificial intelligence platform enables our subscribers to tap into powerful, enhanced building data and insights at the click of a button.

The Science Behind the Matterport Digital Twin: Cortex AI Highlights
Matterport Runs on Cortex
Cortex is our AI-powered software engine that includes a precision deep learning neural network to create digital twins of any building or space. Developed using our proprietary spatial data captured with our Pro2 and Pro3 cameras, Cortex delivers a high degree of precision and accuracy while enabling 3D capture using everyday devices.
Generic neural networks struggle with 3D reconstruction of the real world. Matterport-optimized networks deliver more accurate and robust results. More than just raw training data, Matterport’s datasets allow us to develop new neural network architectures and evaluate them against user behavior and real-world data in millions of situations.
•Deep learning: Connecting and optimizing the detailed neural network data architecture of each space is key to creating robust, highly accurate 3D digital twins. Cortex evaluates and optimizes each 3D model against Matterport’s rich spatial data aggregated from millions of buildings and spaces and the human annotations of those data provided by tens of thousands of subscribers worldwide. Cortex’s evaluative abilities and its data-driven optimization of 3D reconstruction yield consistent, high-precision results across a wide array of building configurations, spaces and environments.
•Dynamic 3D reconstruction: Creating precise 3D spatial data at scale from 2D visuals and static images requires a combination of photorealistic, detailed data from multiple viewpoints and millions of spaces that train and optimize Cortex’s neural network and learning capabilities for improved 3D reconstruction of any space. Cortex’s capabilities combined with real-time spatial alignment algorithms in our 3D capture technology create an intuitive “preview” of any work in progress, allowing subscribers to work with their content interactively and in real-time.
•Computer vision: Cortex enables a suite of powerful features to enhance the value of digital twins. These include automatic measurements for rooms or objects in a room, automatic 2D-from-3D high-definition photo gallery creation, auto face blurring for privacy protection, custom videos, walkthroughs, auto room labeling and object recognition.
•Advanced image processing: Matterport’s computational photography algorithms create a fully automated image processing pipeline to help ensure that each digital twin is of professional grade image quality. Our patented technology makes 3D capture as simple as pressing a single button. Matterport’s software and technology manage the remaining steps, including white balance and camera-specific color correction, high dynamic range tone mapping, de-noising, haze removal, sharpening, saturation and other adjustments to improve image quality.
Spatial Data and AI-Powered Insights
Every Matterport digital twin contains extensive information about a building, room or physical space. The data uses our AI-powered Cortex engine. In addition to the Matterport digital twin itself, our spatial data consists of precision building geometry and structural detail, building contents, fixtures and condition, along with high-definition imagery and photorealistic detail from many vantage points in a space. Cortex employs a technique we call deep spatial indexing. Deep spatial indexing uses artificial intelligence, computer vision and deep learning to identify and convey important details about each space, its structure and its contents with precision and fidelity. We have created a robust spatial data standard that enables Matterport subscribers to harness an interoperable digital system of record for any building.
In addition to creating a highly interactive digital experience for subscribers through the construction of digital twins, we ask ourselves two questions for every subscriber: (1) what is important about their building or physical space and (2) what learnings and insights can we deliver for this space? Our AI-powered Cortex engine helps us answer these questions using our spatial data library to provide aggregated property trends and operational and valuation insights. Moreover, as the Matterport platform ecosystem continues to expand, our subscribers, partners and other third-party developers can bring their own tools to further the breadth and depth of insights they can harvest from our rich spatial data layer.
Extensible Platform Ecosystem
Matterport offers the largest and most accurate library of spatial data in the world, with, as of December 31, 2022, approximately 9.2 million spaces under management and approximately 28 billion captured square feet. The versatility of our spatial data platform and extensive enterprise software development kit and application programming interfaces (“APIs”) has allowed us to develop a robust global ecosystem of channels and partners that extend the Matterport value proposition by geography and vertical market. We intend to continue to deploy a broad set of workflow integrations with our partners and their subscribers to promote an integrated Matterport solution across our target markets. We are also developing a third-party software marketplace to extend the power of our spatial data platform with easy-to-deploy and easy-to-access Matterport software add-ons. The marketplace enables developers to build new applications and spatial data mining tools, enhance the Matterport 3D experience, and create new productivity and property management tools that supplement our core offerings. These value-added capabilities created by third-party developers enable a scalable new revenue stream, with Matterport sharing the subscription and services revenue from each add-on that is deployed to subscribers through the online marketplace. The network effects of our platform ecosystem contributes to the growth of our business, and we believe that it will continue to bolster future growth by enhancing subscriber stickiness and user engagement.
Examples of Matterport add-ons and extensions include:
•Add-ons: Encircle (easy-to-use field documentation tools for faster claims processing); WP Matterport Shortcode (free Wordpress plugin that allows Matterport to be embedded quickly and easily with a Matterport shortcode), WP3D Models (WordPress + Matterport integration plugin); Rela (all-in-one marketing solution for listings); CAPTUR3D (all-in-one Content Management System that extends value to Matterport digital twins); Private Model Emded (feature that allows enterprises to privately share digital twins with a large group of employees on the corporate network without requiring additional user licenses); Views (new workgroup collaboration framework to enable groups and large organizations to create separate, permissions-based workflows to manage different tasks with different teams); and Guided Tours and Tags (tool to elevate the visitor experience by creating directed virtual tours of any commercial or residential space tailored to the interests of their visitors). We unveiled our private beta integration with Amazon Web Services (AWS) IoT TwinMaker to enable enterprise customers to seamlessly connect IoT data into visually immersive and dimensionally accurate Matterport digital twin.
•Services: Matterport ADA Compliant Digital Twin (solution to provide American Disability Act compliant digital twins) and Enterprise Cloud Software Platform (reimagined cloud software platform for the enterprise that creates, publishes, and manages digital twins of buildings and spaces of any size of shape, indoors or outdoors).
Our Competitive Strengths
We believe that we have a number of competitive strengths that will enable our market leadership to grow. Our competitive strengths include:
•Breadth and depth of the Matterport platform. Our core strength is our all-in-one spatial data platform with broad reach across diverse verticals and geographies such as capture to processing to industries without customization. With the ability to integrate seamlessly with various enterprise systems, our platform delivers value across the property lifecycle for diverse end markets, including real estate, AEC, travel and hospitality, repair and insurance, and industrial and facilities. As of December 31, 2022, our global reach extended to subscribers in more than 170 countries, including over 24% of Fortune 1000 companies.
•Market leadership and first-mover advantage. Matterport defined the category of digitizing and datafying the built world almost a decade ago, and we have become the global leader in the category. As of December 31, 2022, we had over 701,000 subscribers on our platform and approximately 9.2 million spaces under management. Our leadership is primarily driven by the fact that we were the first mover in digital twin creation. As a result of our first mover advantage, we have amassed a deep and rich library of spatial data that continues to compound and enhance our leadership position.
•Significant network effect. With each new capture and piece of data added to our platform, the richness of our dataset and the depth of insights from our spaces under management grow. In addition, the combination of our ability to turn data into insights with incremental data from new data captures by our subscribers enables Matterport to develop features for subscribers to our platform. We were a first mover in building a spatial data library for the built world, and our leadership in gathering and deriving insights from data continues to compound and the relevance of those insights attracts more new subscribers.
•Massive spatial data library as the raw material for valuable property insights. The scale of our spatial data library is a significant advantage in deriving insights for our subscribers. Our spatial data library serves as vital ground truth for Cortex, enabling Matterport to create powerful 3D digital twins using a wide range of camera technology, including low-cost digital and smartphone cameras. As of December 31, 2022, our data came from approximately 9.2 million spaces under management and approximately 28 billion captured square feet. As a result, we have taken property insights and analytics to new levels, benefiting subscribers across various industries. For example, facilities managers significantly reduce the time needed to create building layouts, leading to a significant decrease in the cost of site surveying and as-built modeling. AEC subscribers use the analytics of each as-built space to streamline documentation and collaborate with ease.
•Global reach and scale. We are focused on continuing to expand our AI-powered spatial data platform worldwide. We have a significant presence in North America, Europe and Asia, with leadership teams and a go-to-market infrastructure in each of these regions. We have offices in London, Singapore and several across the United States, and we are accelerating our international expansion. As of December 31, 2022, we had over 701,000 subscribers in more than 170 countries. We believe that the geography-agnostic nature of our spatial data platform is a significant advantage as we continue to grow internationally.
•Broad patent portfolio supporting 10 years of R&D and innovation. As of December 31, 2022, we had 54 issued and 37 pending patent applications. Our success is based on almost 10 years of focus on innovation. Innovation has been at the center of Matterport, and we will continue to prioritize our investments in R&D to further our market leading position.
•Superior capture technology. Matterport’s capture technology platform is a software framework that enables support for a wide variety of capture devices required to create a Matterport digital twin of a building or space.
This includes support for LiDAR cameras, 360 cameras, smartphones, Matterport Axis and the Matterport Pro2 and Pro3 cameras. The Pro2 camera was foundational to our spatial data advantage, and we have expanded that advantage with an array of Matterport-enabled third-party capture devices. In August 2022, we launched and began shipment of our Pro3 Camera along with major updates to our industry-leading digital twin cloud platform. The Matterport Pro3 Camera is an advanced 3D capture device, which includes faster boot time, swappable batteries, and a lighter design. The Pro3 camera can perform both indoors and outdoors and is designed for speed, fidelity, versatility and accuracy. Along with our Pro2 Camera, we expect that future sales of our Pro3 Camera will continue to drive increased adoption of our solutions. Matterport is democratizing the 3D capture experience, making high-fidelity and high-accuracy 3D digital twins readily available for any building type and any subscriber need in the property life cycle. While there are other 3D capture solution providers, very few can produce true, dimensionally accurate 3D results, and fewer still can automatically create a final product in photorealistic 3D, and at global scale. This expansive capture technology offering would not be possible without our rich spatial data library available to train the AI-powered Cortex engine to automatically generate accurate digital twins from photos captured with a smartphone or 360 camera.
</document>"""
    resp = await get_completion(PROMPT)
    print(f"Exercise 8.2 has been correctly solved {grade(resp)}: {resp}")

async def exercise_9_1():
    ######################################## INPUT VARIABLES ########################################

    # First input variable - the user's question
    QUESTION = "How long do I have to make an 83b election?"

    # Second input variable - the tax code document that Claude will be using to answer the user's question
    TAX_CODE = """
    (a)General rule
    If, in connection with the performance of services, property is transferred to any person other than the person for whom such services are performed, the excess of—
    (1)the fair market value of such property (determined without regard to any restriction other than a restriction which by its terms will never lapse) at the first time the rights of the person having the beneficial interest in such property are transferable or are not subject to a substantial risk of forfeiture, whichever occurs earlier, over
    (2)the amount (if any) paid for such property,
    shall be included in the gross income of the person who performed such services in the first taxable year in which the rights of the person having the beneficial interest in such property are transferable or are not subject to a substantial risk of forfeiture, whichever is applicable. The preceding sentence shall not apply if such person sells or otherwise disposes of such property in an arm’s length transaction before his rights in such property become transferable or not subject to a substantial risk of forfeiture.
    (b)Election to include in gross income in year of transfer
    (1)In general
    Any person who performs services in connection with which property is transferred to any person may elect to include in his gross income for the taxable year in which such property is transferred, the excess of—
    (A)the fair market value of such property at the time of transfer (determined without regard to any restriction other than a restriction which by its terms will never lapse), over
    (B)the amount (if any) paid for such property.
    If such election is made, subsection (a) shall not apply with respect to the transfer of such property, and if such property is subsequently forfeited, no deduction shall be allowed in respect of such forfeiture.
    (2)Election
    An election under paragraph (1) with respect to any transfer of property shall be made in such manner as the Secretary prescribes and shall be made not later than 30 days after the date of such transfer. Such election may not be revoked except with the consent of the Secretary.

    (c)Special rules
    For purposes of this section—
    (1)Substantial risk of forfeiture
    The rights of a person in property are subject to a substantial risk of forfeiture if such person’s rights to full enjoyment of such property are conditioned upon the future performance of substantial services by any individual.

    (2)Transferability of property
    The rights of a person in property are transferable only if the rights in such property of any transferee are not subject to a substantial risk of forfeiture.

    (3)Sales which may give rise to suit under section 16(b) of the Securities Exchange Act of 1934
    So long as the sale of property at a profit could subject a person to suit under section 16(b) of the Securities Exchange Act of 1934, such person’s rights in such property are—
    (A)subject to a substantial risk of forfeiture, and
    (B)not transferable.
    (4)For purposes of determining an individual’s basis in property transferred in connection with the performance of services, rules similar to the rules of section 72(w) shall apply.
    (d)Certain restrictions which will never lapse
    (1)Valuation
    In the case of property subject to a restriction which by its terms will never lapse, and which allows the transferee to sell such property only at a price determined under a formula, the price so determined shall be deemed to be the fair market value of the property unless established to the contrary by the Secretary, and the burden of proof shall be on the Secretary with respect to such value.

    (2)Cancellation
    If, in the case of property subject to a restriction which by its terms will never lapse, the restriction is canceled, then, unless the taxpayer establishes—
    (A)that such cancellation was not compensatory, and
    (B)that the person, if any, who would be allowed a deduction if the cancellation were treated as compensatory, will treat the transaction as not compensatory, as evidenced in such manner as the Secretary shall prescribe by regulations,
    the excess of the fair market value of the property (computed without regard to the restrictions) at the time of cancellation over the sum of—
    (C)the fair market value of such property (computed by taking the restriction into account) immediately before the cancellation, and
    (D)the amount, if any, paid for the cancellation,
    shall be treated as compensation for the taxable year in which such cancellation occurs.
    (e)Applicability of section
    This section shall not apply to—
    (1)a transaction to which section 421 applies,
    (2)a transfer to or from a trust described in section 401(a) or a transfer under an annuity plan which meets the requirements of section 404(a)(2),
    (3)the transfer of an option without a readily ascertainable fair market value,
    (4)the transfer of property pursuant to the exercise of an option with a readily ascertainable fair market value at the date of grant, or
    (5)group-term life insurance to which section 79 applies.
    (f)Holding period
    In determining the period for which the taxpayer has held property to which subsection (a) applies, there shall be included only the period beginning at the first time his rights in such property are transferable or are not subject to a substantial risk of forfeiture, whichever occurs earlier.

    (g)Certain exchanges
    If property to which subsection (a) applies is exchanged for property subject to restrictions and conditions substantially similar to those to which the property given in such exchange was subject, and if section 354, 355, 356, or 1036 (or so much of section 1031 as relates to section 1036) applied to such exchange, or if such exchange was pursuant to the exercise of a conversion privilege—
    (1)such exchange shall be disregarded for purposes of subsection (a), and
    (2)the property received shall be treated as property to which subsection (a) applies.
    (h)Deduction by employer
    In the case of a transfer of property to which this section applies or a cancellation of a restriction described in subsection (d), there shall be allowed as a deduction under section 162, to the person for whom were performed the services in connection with which such property was transferred, an amount equal to the amount included under subsection (a), (b), or (d)(2) in the gross income of the person who performed such services. Such deduction shall be allowed for the taxable year of such person in which or with which ends the taxable year in which such amount is included in the gross income of the person who performed such services.

    (i)Qualified equity grants
    (1)In general
    For purposes of this subtitle—
    (A)Timing of inclusion
    If qualified stock is transferred to a qualified employee who makes an election with respect to such stock under this subsection, subsection (a) shall be applied by including the amount determined under such subsection with respect to such stock in income of the employee in the taxable year determined under subparagraph (B) in lieu of the taxable year described in subsection (a).

    (B)Taxable year determined
    The taxable year determined under this subparagraph is the taxable year of the employee which includes the earliest of—
    (i)the first date such qualified stock becomes transferable (including, solely for purposes of this clause, becoming transferable to the employer),
    (ii)the date the employee first becomes an excluded employee,
    (iii)the first date on which any stock of the corporation which issued the qualified stock becomes readily tradable on an established securities market (as determined by the Secretary, but not including any market unless such market is recognized as an established securities market by the Secretary for purposes of a provision of this title other than this subsection),
    (iv)the date that is 5 years after the first date the rights of the employee in such stock are transferable or are not subject to a substantial risk of forfeiture, whichever occurs earlier, or
    (v)the date on which the employee revokes (at such time and in such manner as the Secretary provides) the election under this subsection with respect to such stock.
    (2)Qualified stock
    (A)In general
    For purposes of this subsection, the term “qualified stock” means, with respect to any qualified employee, any stock in a corporation which is the employer of such employee, if—
    (i)such stock is received—
    (I)in connection with the exercise of an option, or
    (II)in settlement of a restricted stock unit, and
    (ii)such option or restricted stock unit was granted by the corporation—
    (I)in connection with the performance of services as an employee, and
    (II)during a calendar year in which such corporation was an eligible corporation.
    (B)Limitation
    The term “qualified stock” shall not include any stock if the employee may sell such stock to, or otherwise receive cash in lieu of stock from, the corporation at the time that the rights of the employee in such stock first become transferable or not subject to a substantial risk of forfeiture.

    (C)Eligible corporation
    For purposes of subparagraph (A)(ii)(II)—
    (i)In general
    The term “eligible corporation” means, with respect to any calendar year, any corporation if—
    (I)no stock of such corporation (or any predecessor of such corporation) is readily tradable on an established securities market (as determined under paragraph (1)(B)(iii)) during any preceding calendar year, and
    (II)such corporation has a written plan under which, in such calendar year, not less than 80 percent of all employees who provide services to such corporation in the United States (or any possession of the United States) are granted stock options, or are granted restricted stock units, with the same rights and privileges to receive qualified stock.
    (ii)Same rights and privileges
    For purposes of clause (i)(II)—
    (I)except as provided in subclauses (II) and (III), the determination of rights and privileges with respect to stock shall be made in a similar manner as under section 423(b)(5),
    (II)employees shall not fail to be treated as having the same rights and privileges to receive qualified stock solely because the number of shares available to all employees is not equal in amount, so long as the number of shares available to each employee is more than a de minimis amount, and
    (III)rights and privileges with respect to the exercise of an option shall not be treated as the same as rights and privileges with respect to the settlement of a restricted stock unit.
    (iii)Employee
    For purposes of clause (i)(II), the term “employee” shall not include any employee described in section 4980E(d)(4) or any excluded employee.

    (iv)Special rule for calendar years before 2018
    In the case of any calendar year beginning before January 1, 2018, clause (i)(II) shall be applied without regard to whether the rights and privileges with respect to the qualified stock are the same.

    (3)Qualified employee; excluded employee
    For purposes of this subsection—
    (A)In general
    The term “qualified employee” means any individual who—
    (i)is not an excluded employee, and
    (ii)agrees in the election made under this subsection to meet such requirements as are determined by the Secretary to be necessary to ensure that the withholding requirements of the corporation under chapter 24 with respect to the qualified stock are met.
    (B)Excluded employee
    The term “excluded employee” means, with respect to any corporation, any individual—
    (i)who is a 1-percent owner (within the meaning of section 416(i)(1)(B)(ii)) at any time during the calendar year or who was such a 1 percent owner at any time during the 10 preceding calendar years,
    (ii)who is or has been at any prior time—
    (I)the chief executive officer of such corporation or an individual acting in such a capacity, or
    (II)the chief financial officer of such corporation or an individual acting in such a capacity,
    (iii)who bears a relationship described in section 318(a)(1) to any individual described in subclause (I) or (II) of clause (ii), or
    (iv)who is one of the 4 highest compensated officers of such corporation for the taxable year, or was one of the 4 highest compensated officers of such corporation for any of the 10 preceding taxable years, determined with respect to each such taxable year on the basis of the shareholder disclosure rules for compensation under the Securities Exchange Act of 1934 (as if such rules applied to such corporation).
    (4)Election
    (A)Time for making election
    An election with respect to qualified stock shall be made under this subsection no later than 30 days after the first date the rights of the employee in such stock are transferable or are not subject to a substantial risk of forfeiture, whichever occurs earlier, and shall be made in a manner similar to the manner in which an election is made under subsection (b).

    (B)Limitations
    No election may be made under this section with respect to any qualified stock if—
    (i)the qualified employee has made an election under subsection (b) with respect to such qualified stock,
    (ii)any stock of the corporation which issued the qualified stock is readily tradable on an established securities market (as determined under paragraph (1)(B)(iii)) at any time before the election is made, or
    (iii)such corporation purchased any of its outstanding stock in the calendar year preceding the calendar year which includes the first date the rights of the employee in such stock are transferable or are not subject to a substantial risk of forfeiture, unless—
    (I)not less than 25 percent of the total dollar amount of the stock so purchased is deferral stock, and
    (II)the determination of which individuals from whom deferral stock is purchased is made on a reasonable basis.
    (C)Definitions and special rules related to limitation on stock redemptions
    (i)Deferral stock
    For purposes of this paragraph, the term “deferral stock” means stock with respect to which an election is in effect under this subsection.

    (ii)Deferral stock with respect to any individual not taken into account if individual holds deferral stock with longer deferral period
    Stock purchased by a corporation from any individual shall not be treated as deferral stock for purposes of subparagraph (B)(iii) if such individual (immediately after such purchase) holds any deferral stock with respect to which an election has been in effect under this subsection for a longer period than the election with respect to the stock so purchased.

    (iii)Purchase of all outstanding deferral stock
    The requirements of subclauses (I) and (II) of subparagraph (B)(iii) shall be treated as met if the stock so purchased includes all of the corporation’s outstanding deferral stock.

    (iv)Reporting
    Any corporation which has outstanding deferral stock as of the beginning of any calendar year and which purchases any of its outstanding stock during such calendar year shall include on its return of tax for the taxable year in which, or with which, such calendar year ends the total dollar amount of its outstanding stock so purchased during such calendar year and such other information as the Secretary requires for purposes of administering this paragraph.

    (5)Controlled groups
    For purposes of this subsection, all persons treated as a single employer under section 414(b) shall be treated as 1 corporation.

    (6)Notice requirement
    Any corporation which transfers qualified stock to a qualified employee shall, at the time that (or a reasonable period before) an amount attributable to such stock would (but for this subsection) first be includible in the gross income of such employee—
    (A)certify to such employee that such stock is qualified stock, and
    (B)notify such employee—
    (i)that the employee may be eligible to elect to defer income on such stock under this subsection, and
    (ii)that, if the employee makes such an election—
    (I)the amount of income recognized at the end of the deferral period will be based on the value of the stock at the time at which the rights of the employee in such stock first become transferable or not subject to substantial risk of forfeiture, notwithstanding whether the value of the stock has declined during the deferral period,
    (II)the amount of such income recognized at the end of the deferral period will be subject to withholding under section 3401(i) at the rate determined under section 3402(t), and
    (III)the responsibilities of the employee (as determined by the Secretary under paragraph (3)(A)(ii)) with respect to such withholding.
    (7)Restricted stock units
    This section (other than this subsection), including any election under subsection (b), shall not apply to restricted stock units.
    """



    ######################################## PROMPT ELEMENTS ########################################

    ##### Prompt element 1: `user` role
    # Make sure that your Messages API call always starts with a `user` role in the messages array.
    # The get_completion() function as defined above will automatically do this for you.

    ##### Prompt element 2: Task context
    # Give Claude context about the role it should take on or what goals and overarching tasks you want it to undertake with the prompt.
    # It's best to put context early in the body of the prompt.
    TASK_CONTEXT = "You are a specialist of Finance."

    ##### Prompt element 3: Tone context
    # If important to the interaction, tell Claude what tone it should use.
    # This element may not be necessary depending on the task.
    TONE_CONTEXT = "You should be professional and concise."

    ##### Prompt element 4: Input data to process
    # If there is data that Claude needs to process within the prompt, include it here within relevant XML tags.
    # Feel free to include multiple pieces of data, but be sure to enclose each in its own set of XML tags.
    # This element may not be necessary depending on task. Ordering is also flexible.
    INPUT_DATA = f"""Here is the tex code
<tex_code>
{TAX_CODE}
</tex_code>

Here is the user's question:
<user_question>
{QUESTION}
</user_question>"""

    ##### Prompt element 5: Examples
    # Provide Claude with at least one example of an ideal response that it can emulate. Encase this in <example></example> XML tags. Feel free to provide multiple examples.
    # If you do provide multiple examples, give Claude context about what it is an example of, and enclose each example in its own set of XML tags.
    # Examples are probably the single most effective tool in knowledge work for getting Claude to behave as desired.
    # Make sure to give Claude examples of common edge cases. If your prompt uses a scratchpad, it's effective to give examples of how the scratchpad should look.
    # Generally more examples = better.
    EXAMPLES = ""

    ##### Prompt element 6: Detailed task description and rules
    # Expand on the specific tasks you want Claude to do, as well as any rules that Claude might have to follow.
    # This is also where you can give Claude an "out" if it doesn't have an answer or doesn't know.
    # It's ideal to show this description and rules to a friend to make sure it is laid out logically and that any ambiguous words are clearly defined.
    TASK_DESCRIPTION = ""

    ##### Prompt element 7: Immediate task description or request #####
    # "Remind" Claude or tell Claude exactly what it's expected to immediately do to fulfill the prompt's task.
    # This is also where you would put in additional variables like the user's question.
    # It generally doesn't hurt to reiterate to Claude its immediate task. It's best to do this toward the end of a long prompt.
    # This will yield better results than putting this at the beginning.
    # It is also generally good practice to put the user's query close to the bottom of the prompt.
    IMMEDIATE_TASK = ""

    ##### Prompt element 8: Precognition (thinking step by step)
    # For tasks with multiple steps, it's good to tell Claude to think step by step before giving an answer
    # Sometimes, you might have to even say "Before you give your answer..." just to make sure Claude does this first.
    # Not necessary with all prompts, though if included, it's best to do this toward the end of a long prompt and right after the final immediate task request or description.
    PRECOGNITION = ""

    ##### Prompt element 9: Output formatting
    # If there is a specific way you want Claude's response formatted, clearly tell Claude what that format is.
    # This element may not be necessary depending on the task.
    # If you include it, putting it toward the end of the prompt is better than at the beginning.
    OUTPUT_FORMATTING = ""

    ##### Prompt element 10: Prefilling Claude's response (if any)
    # A space to start off Claude's answer with some prefilled words to steer Claude's behavior or response.
    # If you want to prefill Claude's response, you must put this in the `assistant` role in the API call.
    # This element may not be necessary depending on the task.
    PREFILL = ""



    ######################################## COMBINE ELEMENTS ########################################

    PROMPT = ""

    if TASK_CONTEXT:
        PROMPT += f"""{TASK_CONTEXT}"""

    if TONE_CONTEXT:
        PROMPT += f"""\n\n{TONE_CONTEXT}"""

    if INPUT_DATA:
        PROMPT += f"""\n\n{INPUT_DATA}"""

    if EXAMPLES:
        PROMPT += f"""\n\n{EXAMPLES}"""

    if TASK_DESCRIPTION:
        PROMPT += f"""\n\n{TASK_DESCRIPTION}"""

    if IMMEDIATE_TASK:
        PROMPT += f"""\n\n{IMMEDIATE_TASK}"""

    if PRECOGNITION:
        PROMPT += f"""\n\n{PRECOGNITION}"""

    if OUTPUT_FORMATTING:
        PROMPT += f"""\n\n{OUTPUT_FORMATTING}"""

    # Print full prompt
    print("--------------------------- Full prompt with variable substutions ---------------------------")
    print("USER TURN")
    print(PROMPT)
    print("\nASSISTANT TURN")
    print("\n------------------------------------- Claude's response -------------------------------------")
    print(await get_completion(PROMPT, prefill=PREFILL))

async def exercise_9_2():
    ######################################## INPUT VARIABLES ########################################

    # Input variable - the code that Claude needs to read and assist the user with correcting
    CODE = """
    # Function to print multiplicative inverses
    def print_multiplicative_inverses(x, n):
      for i in range(n):
        print(x / i)
    """



    ######################################## PROMPT ELEMENTS ########################################

    ##### Prompt element 1: `user` role
    # Make sure that your Messages API call always starts with a `user` role in the messages array.
    # The get_completion() function as defined above will automatically do this for you.

    ##### Prompt element 2: Task context
    # Give Claude context about the role it should take on or what goals and overarching tasks you want it to undertake with the prompt.
    # It's best to put context early in the body of the prompt.
    TASK_CONTEXT = "You are a senior developer. You are an expert in Rust programming. You will teach a junior developer how to write a simple Rust program. The junior developer is a new to Rust programming. So, describe code using Python and then porting it into Rust."

    ##### Prompt element 3: Tone context
    # If important to the interaction, tell Claude what tone it should use.
    # This element may not be necessary depending on the task.
    TONE_CONTEXT = "Kind"

    ##### Prompt element 4: Detailed task description and rules
    # Expand on the specific tasks you want Claude to do, as well as any rules that Claude might have to follow.
    # This is also where you can give Claude an "out" if it doesn't have an answer or doesn't know.
    # It's ideal to show this description and rules to a friend to make sure it is laid out logically and that any ambiguous words are clearly defined.
    TASK_DESCRIPTION = ""

    ##### Prompt element 5: Examples
    # Provide Claude with at least one example of an ideal response that it can emulate. Encase this in <example></example> XML tags. Feel free to provide multiple examples.
    # If you do provide multiple examples, give Claude context about what it is an example of, and enclose each example in its own set of XML tags.
    # Examples are probably the single most effective tool in knowledge work for getting Claude to behave as desired.
    # Make sure to give Claude examples of common edge cases. If your prompt uses a scratchpad, it's effective to give examples of how the scratchpad should look.
    # Generally more examples = better.
    EXAMPLES = ""

    ##### Prompt element 6: Input data to process
    # If there is data that Claude needs to process within the prompt, include it here within relevant XML tags.
    # Feel free to include multiple pieces of data, but be sure to enclose each in its own set of XML tags.
    # This element may not be necessary depending on task. Ordering is also flexible.
    INPUT_DATA = f"""Junior: I have a question!
<question>How to convert below code to Rust?</question>

<code>
{CODE}
</code>"""

    ##### Prompt element 7: Immediate task description or request #####
    # "Remind" Claude or tell Claude exactly what it's expected to immediately do to fulfill the prompt's task.
    # This is also where you would put in additional variables like the user's question.
    # It generally doesn't hurt to reiterate to Claude its immediate task. It's best to do this toward the end of a long prompt.
    # This will yield better results than putting this at the beginning.
    # It is also generally good practice to put the user's query close to the bottom of the prompt.
    IMMEDIATE_TASK = ""

    ##### Prompt element 8: Precognition (thinking step by step)
    # For tasks with multiple steps, it's good to tell Claude to think step by step before giving an answer
    # Sometimes, you might have to even say "Before you give your answer..." just to make sure Claude does this first.
    # Not necessary with all prompts, though if included, it's best to do this toward the end of a long prompt and right after the final immediate task request or description.
    PRECOGNITION = ""

    ##### Prompt element 9: Output formatting
    # If there is a specific way you want Claude's response formatted, clearly tell Claude what that format is.
    # This element may not be necessary depending on the task.
    # If you include it, putting it toward the end of the prompt is better than at the beginning.
    OUTPUT_FORMATTING = ""

    ##### Prompt element 10: Prefilling Claude's response (if any)
    # A space to start off Claude's answer with some prefilled words to steer Claude's behavior or response.
    # If you want to prefill Claude's response, you must put this in the `assistant` role in the API call.
    # This element may not be necessary depending on the task.
    PREFILL = ""



    ######################################## COMBINE ELEMENTS ########################################

    PROMPT = ""

    if TASK_CONTEXT:
        PROMPT += f"""{TASK_CONTEXT}"""

    if TONE_CONTEXT:
        PROMPT += f"""\n\n{TONE_CONTEXT}"""

    if TASK_DESCRIPTION:
        PROMPT += f"""\n\n{TASK_DESCRIPTION}"""

    if EXAMPLES:
        PROMPT += f"""\n\n{EXAMPLES}"""

    if INPUT_DATA:
        PROMPT += f"""\n\n{INPUT_DATA}"""

    if IMMEDIATE_TASK:
        PROMPT += f"""\n\n{IMMEDIATE_TASK}"""

    if PRECOGNITION:
        PROMPT += f"""\n\n{PRECOGNITION}"""

    if OUTPUT_FORMATTING:
        PROMPT += f"""\n\n{OUTPUT_FORMATTING}"""

    # Print full prompt
    print("--------------------------- Full prompt with variable substutions ---------------------------")
    print("USER TURN")
    print(PROMPT)
    print("\nASSISTANT TURN")
    print("\n------------------------------------- Claude's response -------------------------------------")
    print(await get_completion(PROMPT, prefill=PREFILL))

async def exercise_10_2_1():
    # db = {
    #     "users": [
    #         {"id": 1, "name": "Alice", "email": "alice@example.com"},
    #         {"id": 2, "name": "Bob", "email": "bob@example.com"},
    #         {"id": 3, "name": "Charlie", "email": "charlie@example.com"}
    #     ],
    #     "products": [
    #         {"id": 1, "name": "Widget", "price": 9.99},
    #         {"id": 2, "name": "Gadget", "price": 14.99},
    #         {"id": 3, "name": "Doohickey", "price": 19.99}
    #     ]
    # }

    # def get_user(user_id):
    #     for user in db["users"]:
    #         if user["id"] == user_id:
    #             return user
    #     return None

    # def get_product(product_id):
    #     for product in db["products"]:
    #         if product["id"] == product_id:
    #             return product
    #     return None

    # def add_user(name, email):
    #     user_id = len(db["users"]) + 1
    #     user = {"id": user_id, "name": name, "email": email}
    #     db["users"].append(user)
    #     return user

    # def add_product(name, price):
    #     product_id = len(db["products"]) + 1
    #     product = {"id": product_id, "name": name, "price": price}
    #     db["products"].append(product)
    #     return product

    system_prompt_tools_general_explanation = """You have access to a set of functions you can use to answer the user's question. This includes access to a
sandboxed computing environment. You do NOT currently have the ability to inspect files or interact with external
resources, except by invoking the below functions.

You can invoke one or more functions by writing a "<function_calls>" block like the following as part of your
reply to the user:
<function_calls>
<invoke name="$FUNCTION_NAME">
<antml:parameter name="$PARAMETER_NAME">$PARAMETER_VALUE</parameter>
...
</invoke>
<nvoke name="$FUNCTION_NAME2">
...
</invoke>
</function_calls>

String and scalar parameters should be specified as is, while lists and objects should use JSON format. Note that
spaces for string values are not stripped. The output is not expected to be valid XML and is parsed with regular
expressions.

The output and/or any errors will appear in a subsequent "<function_results>" block, and remain there as part of
your reply to the user.
You may then continue composing the rest of your reply to the user, respond to any errors, or make further function
calls as appropriate.
If a "<function_results>" does NOT appear after your function calls, then they are likely malformatted and not
recognized as a call."""

    system_prompt_tools_specific_tools_sql = """Here are the functions available in JSONSchema format:

<tools>

<tool_description>
<tool_name>get_user</tool_name>
<description>
Retrieves a user from the database by their user ID.
</description>
<parameters>
<parameter>
<name>user_id</name>
<type>int</type>
<description>The ID of the user to retrieve.</description>
</parameter>
</parameters>
</tool_description>

<tool_description>
<tool_name>get_product</tool_name>
<description>
Retrieves a product from the database by its product ID.
</description>
<parameters>
<parameter>
<name>product_id</name>
<type>int</type>
<description>The ID of the product to retrieve.</description>
</parameter>
</parameters>
</tool_description>

<tool_description>
<tool_name>add_user</tool_name>
<description>
Adds a new user to the database.
</description>
<parameters>
<parameter>
<name>name</name>
<type>str</type>
<description>The name of the user.</description>
</parameter>
<parameter>
<name>email</name>
<type>str</type>
<description>The email address of the user.</description>
</parameter>
</parameters>
</tool_description>

<tool_description>
<tool_name>add_product</tool_name>
<description>
Adds a new product to the database.
</description>
<parameters>
<parameter>
<name>name</name>
<type>str</type>
<description>The name of the product.</description>
</parameter>
<parameter>
<name>price</name>
<type>float</type>
<description>The price of the product.</description>
</parameter>
</parameters>
</tool_description>

</tools>
"""

    system = system_prompt_tools_general_explanation + system_prompt_tools_specific_tools_sql

    examples = [
        "Add a user to the database named Deborah.",
        "Add a product to the database named Thingo",
        "Tell me the name of User 2",
        "Tell me the name of Product 3"
    ]

    stop_sequences = ["</function_calls>"]

    for example in examples:
        # Get & print Claude's response
        function_calling_response = await get_completion(example, system=system, stop_sequences=stop_sequences)
        print(example, "\n----------\n\n", function_calling_response, "\n*********\n*********\n*********\n\n")


async def main():
    # await exercise_1_1()
    # await exercise_1_2()

    # await exercise_2_1()
    # await exercise_2_2()
    # await exercise_2_3()

    # await exercise_3_1()

    # await exercise_4_1()
    # await exercise_4_2()
    # await exercise_4_3()

    # await exercise_5_1()
    # await exercise_5_2()
    # await exercise_5_3()

    # await exercise_6_1()
    # await exercise_6_2()

    # await exercise_7_1()

    # await exercise_8_1()
    # await exercise_8_2()

    # await exercise_9_1()
    # await exercise_9_2()

    await exercise_10_2_1()

if __name__ == "__main__":
    asyncio.run(main())
