from faker import Faker
from pandas import DataFrame


class Generator:
    def __init__(self, locale="zh_CN"):
        # locale = ['zh_CN', 'en_US', 'ja_JP']
        self._fake = Faker(locale)
        self._dataset = []

    def generate_batch(self, batch_size=10, seed=None):
        Faker.seed(seed)
        name, sentence, address = [], [], []
        phone_nubmer, date = [], []
        free_email, job, company = [], [], []
        for i in range(batch_size):
            name.append(self._fake.name())
            address.append(self._fake.address())
            sentence.append(self._fake.sentence())
            phone_nubmer.append(self._fake.phone_number())
            date.append(self._fake.date())
            free_email.append(self._fake.ascii_free_email())
            job.append(self._fake.job()),
            company.append(self._fake.company())

        return DataFrame(
            {
                "date": date,
                "name": name,
                "address": address,
                "phone_number": phone_nubmer,
                "email": free_email,
                "company": company,
                "job": job,
                # 'sentence': sentence,
            }
        )


if __name__ == "__main__":
    generagor = Generator()
    print(generagor.generate_batch())
    print(generagor.generate_batch(10, seed=0))
