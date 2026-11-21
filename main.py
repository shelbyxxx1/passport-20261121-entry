"""Render Tarnovia's passport using only Python's standard library and Pillow."""

from datetime import date
import os
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFont, ImageOps


ROOT = Path(__file__).resolve().parent
FONT_DIR = Path('/usr/share/fonts/truetype/noto')
PAPER = '#F7F3EA'
NAVY = '#1B2A4A'
BLACK = '#141414'
RED = '#8A2A22'
GREEN = '#2A4A33'
PURPLE = '#5A2A4A'
LABEL = '#536075'
NUMBER = 'TV4829137'
SURNAME = 'VUKOVIĆ'
GIVEN = 'PETAR'
NATIONALITY = 'TAR'
BIRTH = date(1987, 3, 12)
ISSUE = date(2021, 6, 14)
EXPIRY = date(2031, 6, 14)
AUTHORITY = ('MINISTRY OF THE INTERIOR —', 'PASSPORT OFFICE, VELGRAD')
TRIPS = (
    ('BRESLAV', 'GORNJI MOST', 'BR-014', date(2021, 9, 2), date(2021, 9, 9), NAVY, 'rectangle'),
    ('KESTRIA', 'ZLATNA PASS', 'KE-207', date(2022, 3, 18), date(2022, 3, 25), GREEN, 'rectangle'),
    ('ONDRIA', 'JUŽNA KAPIJA', 'ON-331', date(2022, 11, 7), date(2022, 11, 19), PURPLE, 'oval'),
)
MONTHS = ('JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC')


def printed_date(value):
    return f'{value.day:02d} {MONTHS[value.month - 1]} {value.year}'


def mrz_digit(value):
    alphabet = '<0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    assert all(character in alphabet for character in value)
    values = [0 if character == '<' else int(character) if character.isdigit()
              else ord(character) - ord('A') + 10 for character in value]
    return str(sum(number * (7, 3, 1)[index % 3]
                   for index, number in enumerate(values)) % 10)


def machine_readable_zone():
    document = NUMBER.ljust(9, '<')
    birth = BIRTH.strftime('%y%m%d')
    expiry = EXPIRY.strftime('%y%m%d')
    optional = '<' * 14
    document_check = mrz_digit(document)
    birth_check = mrz_digit(birth)
    expiry_check = mrz_digit(expiry)
    composite = document + document_check + birth + birth_check + expiry + expiry_check + optional + '<'
    composite_check = mrz_digit(composite)
    assert (document_check, birth_check, expiry_check, composite_check) == ('4', '3', '3', '4')
    surname = SURNAME.translate(str.maketrans({'Ć': 'C'}))
    first = ('P<' + NATIONALITY + surname + '<<' + GIVEN).ljust(44, '<')
    second = (document + document_check + NATIONALITY + birth + birth_check + 'M'
              + expiry + expiry_check + optional + '<' + composite_check)
    assert first == 'P<TARVUKOVIC<<PETAR<<<<<<<<<<<<<<<<<<<<<<<<<'
    assert second == 'TV48291374TAR8703123M3106143<<<<<<<<<<<<<<<4'
    assert len(first) == len(second) == 44
    assert second[:9] == NUMBER
    assert second[10:13] == NATIONALITY
    assert second[13:19] == BIRTH.strftime('%y%m%d')
    assert second[21:27] == EXPIRY.strftime('%y%m%d')
    return first, second


def validate_identity():
    assert NUMBER.startswith('TV') and len(NUMBER) == 9 and NUMBER[2:].isdigit()
    assert printed_date(BIRTH) == '12 MAR 1987'
    assert printed_date(ISSUE) == '14 JUN 2021'
    assert printed_date(EXPIRY) == '14 JUN 2031'
    assert EXPIRY == ISSUE.replace(year=ISSUE.year + 10)
    assert BIRTH.replace(year=BIRTH.year + 38) == date(2025, 3, 12)
    assert BIRTH.replace(year=BIRTH.year + 39) == date(2026, 3, 12)
    previous = ISSUE
    for country, post, control, arrival, departure, ink, shape in TRIPS:
        assert previous < arrival < departure < EXPIRY
        assert (country, post, control) in {
            ('BRESLAV', 'GORNJI MOST', 'BR-014'),
            ('KESTRIA', 'ZLATNA PASS', 'KE-207'),
            ('ONDRIA', 'JUŽNA KAPIJA', 'ON-331'),
        }
        previous = departure
    return machine_readable_zone()


def font(size, weight='regular'):
    names = {
        'regular': 'NotoSans-Regular.ttf',
        'bold': 'NotoSans-Bold.ttf',
        'mono': 'NotoSansMono-Regular.ttf',
        'signature': 'NotoSerif-Italic.ttf',
    }
    return ImageFont.truetype(str(FONT_DIR / names[weight]), size)


def text(draw, position, value, size, weight='regular', fill=BLACK, anchor='ls', max_width=None):
    face = font(size, weight)
    if max_width is not None:
        assert draw.textlength(value, font=face) <= max_width, value
    draw.text(position, value, font=face, fill=fill, anchor=anchor)


def letterspaced(draw, center, baseline, value, size, spacing):
    face = font(size, 'bold')
    width = draw.textlength(value, font=face) + spacing * (len(value) - 1)
    position = center - width / 2
    for character in value:
        draw.text((position, baseline), character, font=face, fill=NAVY, anchor='ls')
        position += draw.textlength(character, font=face) + spacing


def field(draw, left, baseline, label, gloss, value, width=296):
    text(draw, (left, baseline), label, 16, 'bold', LABEL, max_width=width)
    text(draw, (left, baseline + 20), gloss, 14, fill=LABEL, max_width=width)
    text(draw, (left, baseline + 54), value, 23, 'bold', max_width=width)


def data_page(image, mrz):
    draw = ImageDraw.Draw(image)
    draw.line([(483, 83), (511, 43), (541, 83)], fill=NAVY, width=2)
    draw.line([(499, 60), (511, 72), (521, 57)], fill=NAVY, width=1)
    draw.line([(479, 94), (497, 90), (519, 94), (544, 89)], fill=NAVY, width=2)
    letterspaced(draw, 512, 143, 'REPUBLIKA TARNOVIA', 36, 3)
    text(draw, (512, 177), 'REPUBLIC OF TARNOVIA / RÉPUBLIQUE DE TARNOVIE', 18,
         fill=NAVY, anchor='ms', max_width=896)
    text(draw, (512, 214), 'PUTOVNICA — PASSPORT', 22, 'bold', NAVY, 'ms')
    draw.line((64, 239, 960, 239), fill=NAVY, width=1)

    with Image.open(ROOT / 'assets' / 'portrait.png') as source:
        portrait = ImageOps.fit(source.convert('RGB'), (238, 306),
                                Image.Resampling.LANCZOS, centering=(0.5, 0.5))
    assert portrait.width * 45 == portrait.height * 35
    image.paste(portrait, (64, 280))
    draw.rectangle((63, 279, 302, 586), outline=NAVY, width=1)
    text(draw, (183, 610), 'FOTOGRAFIJA / PHOTOGRAPH', 13, fill=LABEL, anchor='ms', max_width=238)
    text(draw, (340, 274), 'PASSPORT No.', 15, 'bold', LABEL)
    text(draw, (340, 312), NUMBER, 32, 'mono', NAVY)
    draw.line((340, 325, 960, 325), fill=LABEL, width=1)

    rows = (
        (('PREZIME', 'SURNAME', SURNAME), ('IME', 'GIVEN NAMES', GIVEN)),
        (('DRŽAVLJANSTVO', 'NATIONALITY', 'TARNOVIAN / TARNOVIEN'), ('SPOL', 'SEX', 'M')),
        (('DATUM ROĐENJA', 'DATE OF BIRTH', printed_date(BIRTH)),
         ('MJESTO ROĐENJA', 'PLACE OF BIRTH', 'DRENOVAC, TARNOVIA')),
        (('DATUM IZDAVANJA', 'DATE OF ISSUE', printed_date(ISSUE)),
         ('VRIJEDI DO', 'DATE OF EXPIRY', printed_date(EXPIRY))),
    )
    for row_index, pair in enumerate(rows):
        baseline = 350 + row_index * 94
        for column, content in enumerate(pair):
            field(draw, 340 + column * 324, baseline, *content)
        draw.line((340, baseline + 68, 960, baseline + 68), fill=LABEL, width=1)

    text(draw, (340, 726), 'IZDAVATELJ', 16, 'bold', LABEL)
    text(draw, (340, 746), 'ISSUING AUTHORITY', 14, fill=LABEL)
    for index, value in enumerate(AUTHORITY):
        text(draw, (340, 779 + index * 30), value, 23, 'bold', max_width=620)

    text(draw, (70, 736), 'Petar Vuković', 30, 'signature', NAVY, max_width=232)
    draw.line((64, 752, 302, 752), fill=NAVY, width=1)
    text(draw, (64, 778), 'POTPIS / SIGNATURE', 14, fill=LABEL)
    draw.line((64, 850, 960, 850), fill=NAVY, width=1)
    for index, line in enumerate(mrz):
        text(draw, (64, 908 + index * 51), line, 33, 'mono', max_width=896)


def stamp_layer(country, direction, when, post, control, ink, shape, angle, phase):
    width, height = (400, 194) if shape == 'oval' else (394, 176)
    mask = Image.new('L', (width + 16, height + 16), 0)
    draw = ImageDraw.Draw(mask)
    center = mask.width / 2
    if shape == 'oval':
        draw.ellipse((8, 8, width + 7, height + 7), outline=255, width=3)
        draw.ellipse((15, 15, width, height), outline=230, width=1)
        offset = 9
    else:
        draw.rectangle((8, 8, width + 7, height + 7), outline=255, width=3)
        draw.rectangle((14, 14, width + 1, height + 1), outline=230, width=1)
        offset = 0
    lines = (
        (43 + offset, country, 27, 'bold'),
        (70 + offset, direction, 19, 'regular'),
        (108 + offset, printed_date(when), 30, 'bold'),
        (137 + offset, post, 20, 'bold'),
        (161 + offset, control, 16, 'regular'),
    )
    for baseline, value, size, weight in lines:
        text(draw, (center, baseline), value, size, weight, 255, 'ms', max_width=width - 36)
    density = Image.new('L', mask.size)
    density.putdata([
        105 if (column * 31 + row * 71 + phase) % 173 == 0
        else 205 + ((column // 19 * 17 + row // 13 * 29 + phase) % 51)
        for row in range(mask.height) for column in range(mask.width)
    ])
    mask = ImageChops.multiply(mask, density)
    layer = Image.new('RGBA', mask.size, ink)
    layer.putalpha(mask)
    return layer.rotate(angle, Image.Resampling.BICUBIC, expand=True)


def stamps_page(image):
    draw = ImageDraw.Draw(image)
    text(draw, (1088, 91), 'ŽIGOVI / STAMPS', 28, 'bold', NAVY)
    draw.line((1088, 122, 1984, 122), fill=NAVY, width=1)
    draw.rectangle((1157, 162, 1915, 290), outline=RED, width=3)
    draw.rectangle((1164, 169, 1908, 283), outline=RED, width=1)
    text(draw, (1536, 207), 'EXIT TAX PAID — 40 TARNOVI', 31, 'bold', RED, 'ms')
    text(draw, (1536, 243), 'VELGRAD, ' + printed_date(ISSUE), 24, 'bold', RED, 'ms')
    text(draw, (1536, 272), 'Art. 17, Travel Act', 19, fill=RED, anchor='ms')
    angles = ((-2.1, 2.4), (2.2, -2.7), (-2.3, 2.0))
    for row, (country, post, control, arrival, departure, ink, shape) in enumerate(TRIPS):
        for column, (direction, when) in enumerate((('ULAZ / ENTRY', arrival), ('IZLAZ / EXIT', departure))):
            stamp = stamp_layer(country, direction, when, post, control, ink, shape,
                                angles[row][column], 47 + row * 23 + column * 61)
            center_x, center_y = (1306, 1766)[column], (427, 650, 878)[row]
            image.paste(stamp, (center_x - stamp.width // 2, center_y - stamp.height // 2), stamp)


def main():
    mrz = validate_identity()
    image = Image.new('RGB', (2048, 1024), PAPER)
    data_page(image, mrz)
    stamps_page(image)
    ImageDraw.Draw(image).line((1024, 32, 1024, 992), fill='#C9C5BD', width=1)
    image = image.resize((1024, 512), Image.Resampling.LANCZOS)
    output = Path(os.environ.get('MAKEFUN_OUTPUT_DIR', '/output'))
    output.mkdir(parents=True, exist_ok=True)
    destination = output / 'entry.png'
    image.save(destination, format='PNG', optimize=True)
    assert destination.stat().st_size <= 1_048_576
    print(destination)


if __name__ == '__main__':
    main()
