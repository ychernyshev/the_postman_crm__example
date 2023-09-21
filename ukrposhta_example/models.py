from django.db import models
from django.template.defaultfilters import slugify

from django.urls import reverse


class RecipientModel(models.Model):
    STREET = [
        ('mkl', 'Мікльоша'),
        ('str', 'Стрийська'),
        ('sok', 'Сокільницька'),
    ]

    street = models.CharField(choices=STREET, max_length=3, default='str')

    BUILD = [
        ('', ''),
        ('3', '3'),
        ('5', '5'),
        ('7', '7'),
        ('9', '9'),
        ('11', '11'),
        ('13', '13'),
        ('15', '15'),
        ('17', '17'),
        ('20', '20'),
        ('23', '23'),
        ('25', '25'),
        ('27', '27'),
        ('73', '73'),
        ('75', '75'),
        ('77', '77'),
        ('79', '79'),
        ('81', '81'),
        ('85', '85'),
        ('87', '87'),
        ('89', '89'),
        ('91', '91'),
        ('93', '93'),
        ('99', '99'),
        ('101', '101'),
        ('103', '103'),
        ('105', '105'),
        ('107', '107'),
        ('111', '111'),
        ('113', '113'),
        ('115', '115'),
        ('117', '117'),
        ('123', '123'),
        ('127', '127'),
        ('129', '129'),
        ('133', '133'),
        ('260', '260'),
        ('262', '262'),
        ('264', '264'),
        ('266', '266'),
        ('268', '268'),
        ('270', '270'),
        ('272', '272'),
        ('274', '274'),
        ('276', '276'),
        ('278', '278'),
        ('280', '280'),
        ('282', '282'),
        ('284', '284'),
        ('286', '286'),
        ('288', '288'),
        ('290', '290'),
        ('292', '292'),
        ('294', '294'),
        ('296', '296'),
        ('298', '298'),
        ('300', '300'),
        ('302', '302'),
        ('304', '304'),
        ('306', '306'),
        ('308', '308'),
        ('310', '310'),
        ('312', '312'),
        ('314', '314'),
        ('316', '316'),
        ('318', '318'),
        ('320', '320'),
        ('322', '322'),
        ('324', '324'),
        ('326', '326'),
        ('328', '328'),
        ('330', '330'),
    ]

    build = models.CharField(choices=BUILD, max_length=3, default='')

    BUILD_LETTER = [
        ('', ''),
        ('A', 'А'),
        ('B', 'Б'),
        ('V', 'В'),
        ('G1', 'Г'),
        ('D', 'Д'),
        ('E1', 'Є'),
        ('E2', 'Е'),
        ('G2', 'Ж'),
    ]

    build_letter = models.CharField(choices=BUILD_LETTER, max_length=2, default='', blank=True)
    flat = models.CharField(max_length=4, blank=True)

    def get_absolute_url(self):
        return f'/{self.id}'

    def __str__(self):
        return f'{self.build}{self.build_letter}/{self.flat} {self.street}'

    class Meta:
        ordering = ['build']
        verbose_name = 'recipient'
        verbose_name_plural = 'Recipient'


class RecipientNameModel(models.Model):
    name = models.CharField(max_length=50)
    parent = models.ForeignKey(RecipientModel, related_name='subscriber_name',
                                db_index=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'subscriber name'
        verbose_name_plural = 'Subscriber names'


class SenderModel(models.Model):
    name = models.CharField(max_length=150, blank=True, unique=True,
                            error_messages={
                                'unique': 'Відправника вже було збережено раніше',
                            })

    # def validate_unique(self, exclude=None):
    #     super(SenderModel, self).validate_unique(exclude=exclude)

    # def save(self, *args, **kwargs):
    #     self.slug = slugify(self.name)
    #     super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'sender'
        verbose_name_plural = 'Senders'


class LettersArchiveModel(models.Model):
    track_number = models.CharField(max_length=13, unique=True)
    slug = models.SlugField(max_length=13, unique=True, blank=True)
    date_of_storage_starting = models.DateField(auto_now=False, null=True, blank=True)
    repeat_delivery = models.BooleanField(default=False, blank=True, null=True)
    # repeat_delivery = models.ForeignKey('RepeatDelivery',
    #                                     related_name='letters_repeat_delivery',
    #                                     db_index=True,
    #                                     on_delete=models.PROTECT,
    #                                     blank=True,
    #                                     null=True)
    recipient_address = models.ForeignKey(RecipientModel,
                                          related_name='recipient_letter',
                                          db_index=True,
                                          on_delete=models.PROTECT)
    # recipient_name = models.CharField(max_length=45, blank=True)
    sender_data = models.ForeignKey(SenderModel,
                                    related_name='sender_letter',
                                    db_index=True,
                                    on_delete=models.CASCADE)
    is_court = models.BooleanField(default=False, blank=True)
    is_court_subpoena = models.BooleanField(default=False, blank=True)
    is_police = models.BooleanField(default=False, blank=True)
    is_police_fine = models.BooleanField(default=False, blank=True)
    is_letter_issued = models.BooleanField(default=False, blank=True)
    is_returned = models.BooleanField(default=False, blank=True)
    # letter_image = models.ImageField(upload_to='letters/letter_image/',
    #                                  default='letters/letter_image/default.png',
    #                                  blank=True,
    #                                  null=True)
    letter_image = models.CharField(max_length=100, unique=True)
    comments = models.TextField(blank=True)

    # def image_filename(self, filename):
    #     fname, dot, extension = filename.rpartition('.')
    #     slug = slugify(self.track_number)
    #     return '%s.%s' % (slug, extension)

    def get_absolute_url(self):
        return f'/{self.slug}'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.track_number)
        super(LettersArchiveModel, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.track_number} | Дата початку зберігання:  {self.date_of_storage_starting}. Cуд: {self.is_court} / Поліція: {self.is_police}. Видано: {self.is_letter_issued} / Повернуто: {self.is_returned}'

    class Meta:
        ordering = ['-id']
        verbose_name = 'лист на збереженні'
        verbose_name_plural = 'Листи на збереженні'


# class RepeatDelivery(models.Model):
#     letters = models.ForeignKey(LettersArchiveModel, db_index=True, on_delete=models.PROTECT)
#     date_of_storage_starting = models.DateField(auto_now=False, null=True, blank=True)
#     is_repeat = models.BooleanField(default=False)
#
#     def _str_(self):
#         return f'{self.is_repeat}: {self.date_of_storage_starting}'
#
#     class Meta:
#         verbose_name = 'repeat letter'
#         verbose_name_plural = 'Repeat letters'
