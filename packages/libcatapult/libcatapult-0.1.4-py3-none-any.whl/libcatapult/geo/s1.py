from datetime import datetime


class S1Product(object):
    """
    S1Product contains details and helper functions for handling S1 product names.
    """
    def __init__(self, name):
        self.product_name = name
        self.satellite = name[0:3]
        self.SAR_mode = name[4:6]
        self.product_type = name[7:16]
        self.start_date = name[17:25]
        self.start_time = name[26:32]
        self.stop_date = name[33:41]
        self.stop_time = name[42:48]
        self.orbit = name[49:55]
        self.image = name[56:62]

    def relative_orbit(self):
        """
        Calculate the relative orbit number from a product

        :return: int of the orbit number. between 0 and 175
        """
        return int(self.orbit) % 175

    def polarisations(self):
        """
        return the polarisations available in this product.

        :return: a list of polarisation codes available in this file.
        """
        if self.product_type.endswith("SV"):
            return ["vv"]
        elif self.product_type.endswith("DV"):
            return ["vh", "vv"]
        elif self.product_type.endswith("SH"):
            return ["hh"]
        elif self.product_type.endswith("DH"):
            return ["hh", "hv"]

    def start_timestamp(self):
        return datetime.strptime(f"{self.start_date}T{self.start_time}", "%Y%m%dT%H%M%S")

    def stop_timestamp(self):
        return datetime.strptime(f"{self.stop_date}T{self.stop_time}", "%Y%m%dT%H%M%S")

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, S1Product):
            return NotImplemented

        return self.product_name == o.product_name and \
            self.SAR_mode == o.SAR_mode and \
            self.product_type == o.product_type and \
            self.start_date == o.start_date and \
            self.start_time == o.start_time and \
            self.stop_date == o.stop_date and \
            self.stop_time == o.stop_time and \
            self.orbit == o.orbit and \
            self.image == o.image


def validate(name):
    """
    Check that an given product name is as expected.

    :param name: the product name to check
    :return: true if the product name is valid.
    """
    # TODO: make this more comprehensive. Validate we have the right parts and so on.
    return not (name.endswith(".zip") or name.endswith(".SAFE") or len(name) != 67)


def common_polarisations(products):
    """
    given a collection of products return the polarisations that can be found in all of them.
    :param products: a collection of products
    :return: list of polarisations that can be found in all of them
    """

    result_set = set(products[0].polarisations())
    for p in products[1:]:
        result_set = result_set & set(p.polarisations())
    return list(result_set)
