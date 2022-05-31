from attrs import define


@define
class Config:
    host: str = '0.0.0.0'
    port: int = 50001


if __name__ == "__main__":
    config = Config()
    print(config, config.host)
