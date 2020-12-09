# Libraries
from datetime import date


def age(self):
    """This method calculates the age from date of birth.

        .. note: use timezone.now date instead?
        .. note: age from date (birth or any other?)
    """
    #  Check both dates have been set.
    if self.dob is None:
        return None
    # Calculate age (plus one).
    date_today = date.today()
    return date_today.year - self.dob.year - \
           ((date_today.month, date_today.day) < \
            (self.dob.month, self.dob.day))
