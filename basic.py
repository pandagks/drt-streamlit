from parameters import load_fixed_customers
from customer import Customer
import math
from datetime import datetime, timedelta

distance_map = {
    ('00_오이도차고지', '02_오이도해양단지.옥터초교입구'): 0.9,
    ('02_오이도해양단지.옥터초교입구', '03_오이도중앙로입구'): 0.3,
    ('03_오이도중앙로입구', '04_오이도종합어시장'): 0.3,
    ('04_오이도종합어시장', '05_함상전망대'): 0.4,
    ('05_함상전망대', '06_오이도박물관'): 0.9,
    ('06_오이도박물관', '07_대부도입구'): 0.4,
    ('07_대부도입구', '08_시화환경사업소'): 0.5,
    ('08_시화환경사업소', '09_시화염색단지입구'): 0.2,
    ('09_시화염색단지입구', '10_삼양사'): 0.4,
    ('10_삼양사', '11_열병합발전소'): 0.5,
    ('11_열병합발전소', '12_우진플라스코'): 0.6,
    ('12_우진플라스코', '13_대한통운.동화산업'): 0.2,
    ('13_대한통운.동화산업', '14_우석철강'): 0.4,
    ('14_우석철강', '15_파워맥스'): 0.6,
    ('15_파워맥스', '16_삼화정공'): 0.4,
    ('16_삼화정공', '17_홈플러스'): 0.4,
    ('17_홈플러스', '18_청솔아파트'): 0.5,
    ('18_청솔아파트', '19_계룡1차아파트'): 0.4,
    ('19_계룡1차아파트', '20_중앙도서관'): 0.4,
    ('20_중앙도서관', '21_이마트'): 0.3,
    ('21_이마트', '22_시화정형외과.이철신경외과'): 0.7,
    ('22_시화정형외과.이철신경외과', '23_소방서.군서고.여성비전센터'): 0.8,
    ('23_소방서.군서고.여성비전센터', '24_정왕역'): 0.4,
    ('24_정왕역', '25_정왕역환승센터'): 0.3,
    ('25_정왕역환승센터', '26_소방서.군서고.여성비전센터'): 0.5,
    ('26_소방서.군서고.여성비전센터', '27_군서미래국제학교'): 1.3,
    ('27_군서미래국제학교', '28_시화정형외과'): 0.4,
    ('28_시화정형외과', '29_금강아파트'): 0.2,
    ('29_금강아파트', '30_이마트'): 0.7,
    ('30_이마트', '31_중앙도서관'): 1.0,
    ('31_중앙도서관', '32_세종3차아파트'): 1.0,
    ('32_세종3차아파트', '33_진로아파트'): 0.6,
    ('33_진로아파트', '34_홈플러스'): 1.8,
    ('34_홈플러스', '35_동국산업'): 0.4,
    ('35_동국산업', '36_중앙알칸'): 0.4,
    ('36_중앙알칸', '37_희망공원'): 0.5,
    ('37_희망공원', '38_대한통운'): 0.4,
    ('38_대한통운', '39_우진프라스코'): 0.2,
    ('39_우진프라스코', '40_열병합발전소'): 0.8,
    ('40_열병합발전소', '41_삼양사'): 1.1,
    ('41_삼양사', '42_시화염색단지입구'): 1.0,
    ('42_시화염색단지입구', '43_시화환경사업소'): 0.8,
    ('43_시화환경사업소', '44_오이도입구'): 1.2,
    ('44_오이도입구', '45_오이도박물관'): 2.0,
    ('45_오이도박물관', '46_함상전망대'): 1.0,
    ('46_함상전망대', '47_오이도종합어시장'): 0.7,
    ('47_오이도종합어시장', '48_오이도중앙로입구'): 0.4,
    ('48_오이도중앙로입구', '49_오이도해양단지.옥터초교입구'): 1.1,
    ('49_오이도해양단지.옥터초교입구', '50_오이도차고지'): 1.6,
}

stops_order = [
    '00_오이도차고지', '02_오이도해양단지.옥터초교입구', '03_오이도중앙로입구',
    '04_오이도종합어시장', '05_함상전망대', '06_오이도박물관', '07_대부도입구',
    '08_시화환경사업소', '09_시화염색단지입구', '10_삼양사', '11_열병합발전소',
    '12_우진플라스코', '13_대한통운.동화산업', '14_우석철강', '15_파워맥스',
    '16_삼화정공', '17_홈플러스', '18_청솔아파트', '19_계룡1차아파트',
    '20_중앙도서관', '21_이마트', '22_시화정형외과.이철신경외과',
    '23_소방서.군서고.여성비전센터', '24_정왕역', '25_정왕역환승센터',
    '26_소방서.군서고.여성비전센터', '27_군서미래국제학교', '28_시화정형외과',
    '29_금강아파트', '30_이마트', '31_중앙도서관', '32_세종3차아파트',
    '33_진로아파트', '34_홈플러스', '35_동국산업', '36_중앙알칸',
    '37_희망공원', '38_대한통운', '39_우진프라스코', '40_열병합발전소',
    '41_삼양사', '42_시화염색단지입구', '43_시화환경사업소', '44_오이도입구',
    '45_오이도박물관', '46_함상전망대', '47_오이도종합어시장', '48_오이도중앙로입구',
    '49_오이도해양단지.옥터초교입구', '50_오이도차고지'
]

CUSTOMERS = load_fixed_customers()
BUS_SPEED_KMH = 30
SERVICE_TIME_PER_PERSON = 0.2
SERVICE_TIME_MIN = 0.2

def get_distance(stop1, stop2):
    return distance_map.get((stop1, stop2), distance_map.get((stop2, stop1), 0.0))

total_abandoned = 0

def process_boarding_alighting(stop, current_time, total_boarded):
    global total_abandoned  # 전역 변수 사용

    current_minute = current_time.hour * 60 + current_time.minute

    # 하차 승객
    alighting_customers = [c for c in CUSTOMERS if c.getoff_stop == stop and c.boarded and not c.dropped_off]

    # 탑승할 승객 중 현재 정류장이고, 예상 승차시간 <= 현재 시각이며 아직 탑승하지 않고 포기하지 않은 승객
    boarding_customers = [c for c in CUSTOMERS if c.boarding_stop == stop and c.time <= current_minute and not c.boarded and not c.abandoned]

    alighting_count = len(alighting_customers)
    boarding_count = 0
    abandoned_count = 0

    for c in alighting_customers:
        c.dropped_off = True

    for c in boarding_customers:
        # 버스 도착 시간 - 예상 승차 시간 > 45분이면 탑승 포기
        if current_minute - c.time > 45:
            c.abandoned = True
            total_abandoned += 1
            abandoned_count += 1
            continue

        # 탑승 허용
        c.boarded = True
        c.boarding_time = current_minute
        boarding_count += 1

    # 처리 시간 계산 (승하차 승객 없더라도 최소 SERVICE_TIME_MIN 보장)
    processing_time = round(SERVICE_TIME_MIN * max(1, (boarding_count + alighting_count)), 2)

    completed_time = current_time + timedelta(minutes=processing_time)

    total_boarded += boarding_count

    print(f"  하차 승객: {alighting_count}, 승차 승객: {boarding_count}, 탑승 포기 승객: {abandoned_count}")
    print(f"  처리 시간: {processing_time}분, 완료 시각: {completed_time.strftime('%H:%M')}")

    return completed_time, total_boarded

def simulate_fixed_route():
    current_time = datetime.strptime("10:00", "%H:%M")
    end_time = datetime.strptime("17:00", "%H:%M")

    current_stop_index = 0
    current_stop = stops_order[current_stop_index]
    total_distance = 0.0
    total_boarded = 0

    print(f"[{current_time.strftime('%H:%M')}] {current_stop} - 출발")
    current_time, total_boarded = process_boarding_alighting(current_stop, current_time, total_boarded)

    while current_time < end_time:
        next_index = (current_stop_index + 1) % len(stops_order)
        next_stop = stops_order[next_index]

        distance = get_distance(current_stop, next_stop)
        total_distance += distance

        travel_minutes = round((distance / BUS_SPEED_KMH) * 60, 2)
        arrival_time = current_time + timedelta(minutes=travel_minutes)

        print(f"[{arrival_time.strftime('%H:%M')}] {next_stop} - 도착")
        current_time, total_boarded = process_boarding_alighting(next_stop, arrival_time, total_boarded)

        current_stop_index = next_index
        current_stop = next_stop

    print("\n===== 시뮬레이션 요약 =====")
    print(f"총 이동 거리: {round(total_distance, 2)} km")
    print(f"총 승차 승객 수: {total_boarded}명")
    print(f"총 탑승 포기 승객 수: {total_abandoned}명")

if __name__ == "__main__":
    simulate_fixed_route()