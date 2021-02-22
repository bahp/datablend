# Libraries
import pandas as pd


def report_print(info, tidy, comp, verbose=10):
    """"""
    pass


def report_parental_fluid(tidy, verbose=10):
    """This evaluates that when parental_fluid_volume
       is higher than 0, then parental_fluid is set to
       True.
    """
    if 'parental_fluid_volume' not in tidy:
        return

    if 'parental_fluid' not in tidy:
        tidy['parental_fluid'] = None

    # Compare
    aux1 = tidy.parental_fluid == True
    aux2 = tidy.parental_fluid_volume > 0
    comp = aux1[aux2].compare(aux2[aux2])

    # Comparing parental_fluid
    print("   {0:20} | {1:3} inconsistencies".format( \
        'parental_fluid', comp.size))

    if comp.size > 0 and verbose > 5:
        print(tidy.loc[comp.index, ['parental_fluid',
                                    'parental_fluid_volume']])


def report_event_death(tidy, verbose=10):
    """This evaluates that when event_death is true
       the outcome needs to be equal to 'Died' and
       reports it otherwise."""
    if 'event_death' not in tidy:
        return
    if 'outcome' not in tidy:
        return

    aux1 = tidy.outcome == 'Died'
    aux2 = tidy.event_death == True
    comp = aux1[aux2].compare(aux2[aux2])

    # Comparing parental_fluid
    print("   {0:20} | {1:3} inconsistencies".format( \
        'event_death', comp.size))

    if comp.size > 0 and verbose > 5:
        print(tidy.loc[comp.index, ['event_death',
                                    'outcome']])


def report_shock(tidy, verbose):
    """This method...."""
    if 'shock' not in tidy:
        return
    if 'shock_multiple' not in tidy:
        return

    aux1 = tidy.shock == True
    aux2 = tidy.shock_multiple == True
    comp = aux1[aux2].compare(aux2[aux2])

    # Comparing parental_fluid
    print("   {0:20} | {1:3} inconsistencies".format( \
        'multiple_shock', comp.size))


def report_shock_multiple(tidy, verbose):
    if 'shock_multiple' not in tidy:
        return
    if 'event_shock' not in tidy:
        return
    pass


def report_pcr_dengue(tidy, verbose):
    if 'pcr_dengue_load' not in tidy:
        return
    if 'pcr_dengue_serotype' not in tidy:
        return

    aux1 = tidy.pcr_dengue_serotype.notna()
    aux2 = tidy.pcr_dengue_load <= 0.1
    comp = aux1[aux2].compare(aux2[aux2])

    # Comparing parental_fluid
    print("   {0:20} | {1:3} inconsistencies".format( \
        'pcr_dengue_serotype', comp.size))


def oucru_report(tidy, verbose=10):
    """"""

    report_parental_fluid(tidy, verbose)
    report_event_death(tidy, verbose)
    report_shock(tidy, verbose)
    report_pcr_dengue(tidy, verbose)




