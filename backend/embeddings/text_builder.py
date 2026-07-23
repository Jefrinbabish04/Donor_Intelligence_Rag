def donor_to_text(donor):
    return f"""
Donor ID: {donor.donor_id}
Name: {donor.name}
Blood Group: {donor.blood_group}
City: {donor.city}
State:{donor.state}
Hospital:{donor.hospital}
Medical History:{donor.medical_history}
Notes:{donor.notes}
Donation Count:{donor.donation_count}
"""