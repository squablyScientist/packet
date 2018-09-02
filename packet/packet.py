from .models import Freshman, UpperSignature, FreshSignature, MiscSignature, db


def sign(signer_username, freshman_username):
    freshman = Freshman.query.filter_by(rit_username=freshman_username).first()
    if freshman is None:
        return False
    packet = freshman.current_packet()
    if packet is None:
        return False
    if not packet.is_open():
        return False

    upper_signature = UpperSignature.query.filter(UpperSignature.member == signer_username).first()
    fresh_signature = FreshSignature.query.filter(FreshSignature.freshman_username == signer_username).first()

    if upper_signature:
        upper_signature.signed = True
    elif fresh_signature:
        fresh_signature.signed = True
    else:
        db.session.add(MiscSignature(packet=packet, member=signer_username))
    db.session.commit()

    return True


def get_signatures(freshman_username):
    packet = Freshman.query.filter_by(rit_username=freshman_username).first().current_packet()
    eboard = UpperSignature.query.filter_by(packet_id=packet.id, eboard=True).order_by(UpperSignature.signed.desc())
    upper_signatures = UpperSignature.query.filter_by(packet_id=packet.id, eboard=False).order_by(UpperSignature.signed.desc())
    fresh_signatures = FreshSignature.query.filter_by(packet_id=packet.id).order_by(FreshSignature.signed.desc())
    misc_signatures = MiscSignature.query.filter_by(packet_id=packet.id)
    return {'eboard': eboard,
            'upperclassmen': upper_signatures,
            'freshmen': fresh_signatures,
            'misc': misc_signatures}


def get_number_signed(freshman_username):
    return Freshman.query.filter_by(rit_username=freshman_username).first().current_packet().signatures_received()


def get_number_required(freshman_username):
    return Freshman.query.filter_by(rit_username=freshman_username).first().current_packet().signatures_required()
