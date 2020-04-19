# Copyright (C) 2017-2020 University of Glasgow
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

import unittest
import os
import sys

from pathlib       import Path
from unittest.mock import patch, Mock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import ietfdata
from ietfdata.datatracker import *


# =================================================================================================================================
# Unit tests:

class TestDatatracker(unittest.TestCase):
    dt : DataTracker

    # -----------------------------------------------------------------------------------------------------------------------------
    # Tests relating to email addresses:

    @classmethod
    def setUpClass(self) -> None:
        self.dt = DataTracker(cache_dir=Path("cache"))

    def test_email(self) -> None:
        e  = self.dt.email(EmailURI("/api/v1/person/email/csp@csperkins.org/"))
        if e is not None:
            self.assertEqual(e.resource_uri, EmailURI("/api/v1/person/email/csp@csperkins.org/"))
            self.assertEqual(e.address,      "csp@csperkins.org")
            self.assertEqual(e.person,       PersonURI("/api/v1/person/person/20209/"))
            self.assertEqual(e.time,         datetime.fromisoformat("1970-01-01T23:59:59"))
            # self.assertEqual(e.origin,     "author: draft-ietf-mmusic-rfc4566bis")
            self.assertEqual(e.primary,      True)
            self.assertEqual(e.active,       True)
        else:
            self.fail("Cannot find email address")


    def test_email_for_person(self) -> None:
        p  = self.dt.person_from_email("csp@csperkins.org")
        if p is not None:
            es = list(self.dt.email_for_person(p))
            self.assertEqual(len(es), 5)
            self.assertEqual(len([x for x in es if x.address == "csp@csperkins.org"]), 1)
            self.assertEqual(len([x for x in es if x.address == "csp@isi.edu"]), 1)
            self.assertEqual(len([x for x in es if x.address == "colin.perkins@glasgow.ac.uk"]), 1)
            self.assertEqual(len([x for x in es if x.address == "csp@cperkins.net"]), 1)
            self.assertEqual(len([x for x in es if x.address == "c.perkins@cs.ucl.ac.uk"]), 1)
        else:
            self.fail("Cannot find person")


    def test_email_history_for_address(self) -> None:
        h  = list(self.dt.email_history_for_address("csp@isi.edu"))
        self.assertEqual(len(h), 2)
        self.assertEqual(len([x for x in h if x.resource_uri == EmailURI("/api/v1/person/historicalemail/71987/")]), 1)
        self.assertEqual(len([x for x in h if x.resource_uri == EmailURI("/api/v1/person/historicalemail/2090/")]), 1)


    def test_email_history_for_person(self) -> None:
        p  = self.dt.person_from_email("casner@acm.org")
        if p is not None:
            h = list(self.dt.email_history_for_person(p))
            self.assertEqual(len(h), 4)
            self.assertEqual(len([x for x in h if x.address == "casner@packetdesign.com"]), 1)
            self.assertEqual(len([x for x in h if x.address == "casner@acm.org"]), 1)
            self.assertEqual(len([x for x in h if x.address == "casner@cisco.com"]), 1)
            self.assertEqual(len([x for x in h if x.address == "casner@precept.com"]), 1)
        else:
            self.fail("Cannot find person")


    def test_emails(self) -> None:
        e = list(self.dt.emails(addr_contains="csperkins.org"))
        self.assertEqual(len(e), 1)
        self.assertEqual(e[0].resource_uri, EmailURI('/api/v1/person/email/csp@csperkins.org/'))


    # -----------------------------------------------------------------------------------------------------------------------------
    # Tests relating to people:

    def test_person_from_email(self) -> None:
        p  = self.dt.person_from_email("csp@csperkins.org")
        if p is not None:
            self.assertEqual(p.id,              20209)
            self.assertEqual(p.resource_uri,    PersonURI("/api/v1/person/person/20209/"))
            self.assertEqual(p.name,            "Colin Perkins")
            self.assertEqual(p.name_from_draft, "Colin Perkins")
            self.assertEqual(p.ascii,           "Colin Perkins")
            self.assertEqual(p.ascii_short,     "")
            self.assertEqual(p.user,            "")
            self.assertEqual(p.time,            datetime.fromisoformat("2012-02-26T00:03:54"))
            self.assertEqual(p.photo,           "https://www.ietf.org/lib/dt/media/photo/Colin-Perkins-sm.jpg")
            self.assertEqual(p.photo_thumb,     "https://www.ietf.org/lib/dt/media/photo/Colin-Perkins-sm_PMIAhXi.jpg")
            # self.assertEqual(p.biography,     "Colin Perkins is a ...")
            self.assertEqual(p.consent,         True)
        else:
            self.fail("Cannot find person")

    def test_person(self) -> None:
        p  = self.dt.person(PersonURI("/api/v1/person/person/20209/"))
        if p is not None:
            self.assertEqual(p.id,              20209)
            self.assertEqual(p.resource_uri,    PersonURI("/api/v1/person/person/20209/"))
            self.assertEqual(p.name,            "Colin Perkins")
            self.assertEqual(p.name_from_draft, "Colin Perkins")
            self.assertEqual(p.ascii,           "Colin Perkins")
            self.assertEqual(p.ascii_short,     "")
            self.assertEqual(p.user,            "")
            self.assertEqual(p.time,            datetime.fromisoformat("2012-02-26T00:03:54"))
            self.assertEqual(p.photo,           "https://www.ietf.org/lib/dt/media/photo/Colin-Perkins-sm.jpg")
            self.assertEqual(p.photo_thumb,     "https://www.ietf.org/lib/dt/media/photo/Colin-Perkins-sm_PMIAhXi.jpg")
            # self.assertEqual(p.biography,     "Colin Perkins is a ...")
            self.assertEqual(p.consent,         True)
        else:
            self.fail("Cannot find person")


    def test_person_history(self) -> None:
        p  = self.dt.person(PersonURI("/api/v1/person/person/20209/"))
        if p is not None:
            h  = list(self.dt.person_history(p))
            # As of 2019-08-18, there are two history items for csp@csperkins.org
            self.assertEqual(len(h), 3)

            self.assertEqual(h[0].id,              20209)
            self.assertEqual(h[0].resource_uri,    PersonURI("/api/v1/person/historicalperson/11731/"))
            self.assertEqual(h[0].name,            "Colin Perkins")
            self.assertEqual(h[0].name_from_draft, "Colin Perkins")
            self.assertEqual(h[0].ascii,           "Colin Perkins")
            self.assertEqual(h[0].ascii_short,     "")
            self.assertEqual(h[0].user,            "")
            self.assertEqual(h[0].time,            datetime.fromisoformat("2012-02-26T00:03:54"))
            self.assertEqual(h[0].photo,           "photo/Colin-Perkins-sm.jpg")
            self.assertEqual(h[0].photo_thumb,     "photo/Colin-Perkins-sm_PMIAhXi.jpg")
            # self.assertEqual(h[0].biography,     "Colin Perkins is a ...")
            self.assertEqual(h[0].consent,         True)
            self.assertEqual(h[0].history_change_reason, None)
            self.assertEqual(h[0].history_user,    "")
            self.assertEqual(h[0].history_id,      11731)
            self.assertEqual(h[0].history_type,    "~")
            self.assertEqual(h[0].history_date,    datetime.fromisoformat("2019-09-29T14:39:48.278674"))

            self.assertEqual(h[1].id,              20209)
            self.assertEqual(h[1].resource_uri,    PersonURI("/api/v1/person/historicalperson/10878/"))
            self.assertEqual(h[1].name,            "Colin Perkins")
            self.assertEqual(h[1].name_from_draft, "Colin Perkins")
            self.assertEqual(h[1].ascii,           "Colin Perkins")
            self.assertEqual(h[1].ascii_short,     None)
            self.assertEqual(h[1].user,            "")
            self.assertEqual(h[1].time,            datetime.fromisoformat("2012-02-26T00:03:54"))
            self.assertEqual(h[1].photo,           "photo/Colin-Perkins-sm.jpg")
            self.assertEqual(h[1].photo_thumb,     "photo/Colin-Perkins-sm_PMIAhXi.jpg")
            # self.assertEqual(h[1].biography,     "Colin Perkins is a ...")
            self.assertEqual(h[1].consent,         True)
            self.assertEqual(h[1].history_change_reason, None)
            self.assertEqual(h[1].history_user,    "")
            self.assertEqual(h[1].history_id,      10878)
            self.assertEqual(h[1].history_type,    "~")
            self.assertEqual(h[1].history_date,    datetime.fromisoformat("2019-03-29T02:44:28.426049"))

            self.assertEqual(h[2].id,              20209)
            self.assertEqual(h[2].resource_uri,    PersonURI("/api/v1/person/historicalperson/127/"))
            self.assertEqual(h[2].name,            "Colin Perkins")
            self.assertEqual(h[2].name_from_draft, "Colin Perkins")
            self.assertEqual(h[2].ascii,           "Colin Perkins")
            self.assertEqual(h[2].ascii_short,     "")
            self.assertEqual(h[2].user,            "")
            self.assertEqual(h[2].time,            datetime.fromisoformat("2012-02-26T00:03:54"))
            self.assertEqual(h[2].photo,           "")
            self.assertEqual(h[2].photo_thumb,     "")
            self.assertEqual(h[2].biography,       "")
            self.assertEqual(h[2].consent,         True)
            self.assertEqual(h[2].history_change_reason, None)
            self.assertEqual(h[2].history_user,    "")
            self.assertEqual(h[2].history_id,      127)
            self.assertEqual(h[2].history_type,    "~")
            self.assertEqual(h[2].history_date,    datetime.fromisoformat("2018-06-19T15:39:39.929158"))
        else:
            self.fail("Cannot find person")


    def test_person_aliases(self) -> None:
        p  = self.dt.person(PersonURI("/api/v1/person/person/20209/"))
        if p is not None:
            aliases  = list(self.dt.person_aliases(p))
            self.assertEqual(len(aliases), 2)
            self.assertEqual(len([x for x in aliases if x.id ==    62]), 1)
            self.assertEqual(len([x for x in aliases if x.id == 22620]), 1)
        else:
            self.fail("Cannot find person")


    def test_person_events(self) -> None:
        p = self.dt.person(PersonURI("/api/v1/person/person/3/"))
        if p is not None:
            events = list(self.dt.person_events(p))
            self.assertEqual(len(events), 1)
            self.assertEqual(events[0].desc,         "Sent GDPR notice email to [u'vint@google.com', u'vcerf@mci.net', u'vcerf@nri.reston.va.us', u'vinton.g.cerf@wcom.com'] with confirmation deadline 2018-10-22")
            self.assertEqual(events[0].id,           478)
            self.assertEqual(events[0].person,       PersonURI("/api/v1/person/person/3/"))
            self.assertEqual(events[0].resource_uri, PersonEventURI("/api/v1/person/personevent/478/"))
            self.assertEqual(events[0].time,         datetime.fromisoformat("2018-09-24T09:28:32.502465"))
            self.assertEqual(events[0].type,         "gdpr_notice_email")
        else:
            self.fail("Cannot find person")


    def test_people(self) -> None:
        p  = list(self.dt.people(name_contains="Colin Perkins"))
        self.assertEqual(len(p), 1)
        self.assertEqual(p[ 0].resource_uri, PersonURI("/api/v1/person/person/20209/"))


    # -----------------------------------------------------------------------------------------------------------------------------
    # Tests relating to documents:

    # There is one test_document_*() method for each document type

    def test_document_agenda(self) -> None:
        d  = self.dt.document(DocumentURI("/api/v1/doc/document/agenda-90-precis/"))
        if d is not None:
            self.assertEqual(d.expires,            None)
            self.assertEqual(d.order,              1)
            self.assertEqual(d.intended_std_level, None)
            self.assertEqual(d.uploaded_filename,  "agenda-90-precis.txt")
            self.assertEqual(d.states,             [DocumentStateURI("/api/v1/doc/state/81/")])
            self.assertEqual(d.abstract,           "")
            self.assertEqual(d.notify,             "")
            self.assertEqual(d.type,               DocumentTypeURI("/api/v1/name/doctypename/agenda/"))
            self.assertEqual(d.rev,                "2")
            self.assertEqual(d.internal_comments,  "")
            self.assertEqual(d.id,                 218)
            self.assertEqual(d.std_level,          None)
            self.assertEqual(d.ad,                 None)
            self.assertEqual(d.time,               datetime.fromisoformat("2014-07-21T11:14:17"))
            self.assertEqual(d.title,              "Agenda for PRECIS at IETF-90")
            self.assertEqual(d.shepherd,           None)
            self.assertEqual(d.pages,              None)
            self.assertEqual(d.tags,               [])
            self.assertEqual(d.resource_uri,       DocumentURI("/api/v1/doc/document/agenda-90-precis/"))
            self.assertEqual(d.rfc,                None)
            self.assertEqual(d.words,              None)
            self.assertEqual(d.submissions,        [])
            self.assertEqual(d.name,               "agenda-90-precis")
            self.assertEqual(d.stream,             None)
            self.assertEqual(d.group,              GroupURI("/api/v1/group/group/1798/"))
            self.assertEqual(d.note,               "")
            self.assertEqual(d.external_url,       "")

            url = d.url()
            self.assertEqual(url, "https://datatracker.ietf.org/meeting/90/materials/agenda-90-precis.txt")
            self.assertEqual(self.dt.session.get(url).status_code, 200)
        else:
            self.fail("Cannot find document")


    def test_document_bluesheets(self) -> None:
        d  = self.dt.document(DocumentURI("/api/v1/doc/document/bluesheets-95-xrblock-01/"))
        if d is not None:
            self.assertEqual(d.internal_comments,  "")
            self.assertEqual(d.id,                 68163)
            self.assertEqual(d.name,               "bluesheets-95-xrblock-01")
            self.assertEqual(d.notify,             "")
            self.assertEqual(d.order,              1)
            self.assertEqual(d.rev,                "00")
            self.assertEqual(d.external_url,       "")
            self.assertEqual(d.expires,            None)
            self.assertEqual(d.type,               DocumentTypeURI("/api/v1/name/doctypename/bluesheets/"))
            self.assertEqual(d.group,              GroupURI("/api/v1/group/group/1815/"))
            self.assertEqual(d.resource_uri,       DocumentURI("/api/v1/doc/document/bluesheets-95-xrblock-01/"))
            self.assertEqual(d.title,              "Bluesheets IETF95 : xrblock : Wed 16:20")
            self.assertEqual(d.abstract,           "")
            self.assertEqual(d.uploaded_filename,  "bluesheets-95-xrblock-01.pdf")
            self.assertEqual(d.rfc,                None)
            self.assertEqual(d.shepherd,           None)
            self.assertEqual(d.submissions,        [])
            self.assertEqual(d.intended_std_level, None)
            self.assertEqual(d.ad,                 None)
            self.assertEqual(d.note,               "")
            self.assertEqual(d.words,              None)
            self.assertEqual(d.tags,               [])
            self.assertEqual(d.time,               datetime.fromisoformat("2016-08-22T05:39:08"))
            self.assertEqual(d.pages,              None)
            self.assertEqual(d.stream,             None)
            self.assertEqual(d.std_level,          None)
            self.assertEqual(d.states,             [DocumentStateURI("/api/v1/doc/state/139/")])

            url = d.url()
            self.assertEqual(url, "https://www.ietf.org/proceedings/95/bluesheets/bluesheets-95-xrblock-01.pdf")
            self.assertEqual(self.dt.session.get(url).status_code, 200)
        else:
            self.fail("Cannot find document")


    def test_document_charter(self) -> None:
        d  = self.dt.document(DocumentURI("/api/v1/doc/document/charter-ietf-vgmib/"))
        if d is not None:
            self.assertEqual(d.internal_comments,  "")
            self.assertEqual(d.id,                 1)
            self.assertEqual(d.name,               "charter-ietf-vgmib")
            self.assertEqual(d.notify,             "")
            self.assertEqual(d.order,              1)
            self.assertEqual(d.rev,                "01")
            self.assertEqual(d.external_url,       "")
            self.assertEqual(d.expires,            None)
            self.assertEqual(d.type,               DocumentTypeURI("/api/v1/name/doctypename/charter/"))
            self.assertEqual(d.group,              GroupURI("/api/v1/group/group/925/"))
            self.assertEqual(d.resource_uri,       DocumentURI("/api/v1/doc/document/charter-ietf-vgmib/"))
            self.assertEqual(d.title,              "100VG-AnyLAN MIB")
            self.assertEqual(d.abstract,           "100VG-AnyLAN MIB")
            self.assertEqual(d.uploaded_filename,  "")
            self.assertEqual(d.rfc,                None)
            self.assertEqual(d.shepherd,           None)
            self.assertEqual(d.submissions,        [])
            self.assertEqual(d.intended_std_level, None)
            self.assertEqual(d.ad,                 None)
            self.assertEqual(d.note,               "")
            self.assertEqual(d.words,              None)
            self.assertEqual(d.tags,               [])
            self.assertEqual(d.time,               datetime.fromisoformat("1998-01-26T12:00:00"))
            self.assertEqual(d.pages,              None)
            self.assertEqual(d.stream,             None)
            self.assertEqual(d.std_level,          None)
            self.assertEqual(d.states,             [DocumentStateURI("/api/v1/doc/state/88/")])

            url = d.url()
            self.assertEqual(url, "https://www.ietf.org/charter/charter-ietf-vgmib-01.txt")
            self.assertEqual(self.dt.session.get(url).status_code, 200)
        else:
            self.fail("Cannot find document")


    def test_document_conflrev(self) -> None:
        d  = self.dt.document(DocumentURI("/api/v1/doc/document/conflict-review-kiyomoto-kcipher2/"))
        if d is not None:
            self.assertEqual(d.internal_comments,  "")
            self.assertEqual(d.id,                 17898)
            self.assertEqual(d.name,               "conflict-review-kiyomoto-kcipher2")
            self.assertEqual(d.notify,             "\"Nevil Brownlee\" <rfc-ise@rfc-editor.org>, draft-kiyomoto-kcipher2@tools.ietf.org")
            self.assertEqual(d.order,              1)
            self.assertEqual(d.rev,                "00")
            self.assertEqual(d.external_url,       "")
            self.assertEqual(d.expires,            None)
            self.assertEqual(d.type,               DocumentTypeURI("/api/v1/name/doctypename/conflrev/"))
            self.assertEqual(d.group,              GroupURI("/api/v1/group/group/2/"))
            self.assertEqual(d.resource_uri,       DocumentURI("/api/v1/doc/document/conflict-review-kiyomoto-kcipher2/"))
            self.assertEqual(d.title,              "IETF conflict review for draft-kiyomoto-kcipher2")
            self.assertEqual(d.abstract,           "")
            self.assertEqual(d.uploaded_filename,  "")
            self.assertEqual(d.rfc,                None)
            self.assertEqual(d.shepherd,           None)
            self.assertEqual(d.submissions,        [])
            self.assertEqual(d.intended_std_level, None)
            self.assertEqual(d.ad,                 PersonURI("/api/v1/person/person/19177/"))
            self.assertEqual(d.note,               "")
            self.assertEqual(d.words,              None)
            self.assertEqual(d.tags,               [])
            self.assertEqual(d.time,               datetime.fromisoformat("2013-07-15T14:47:31"))
            self.assertEqual(d.pages,              None)
            self.assertEqual(d.stream,             StreamURI("/api/v1/name/streamname/ietf/"))
            self.assertEqual(d.std_level,          None)
            self.assertEqual(d.states,             [DocumentStateURI("/api/v1/doc/state/97/")])

            url = d.url()
            self.assertEqual(url, "https://www.ietf.org/cr/conflict-review-kiyomoto-kcipher2-00.txt")
            self.assertEqual(self.dt.session.get(url).status_code, 200)
        else:
            self.fail("Cannot find document")


    def test_document_draft(self) -> None:
        d  = self.dt.document(DocumentURI("/api/v1/doc/document/draft-ietf-avt-rtp-new/"))
        if d is not None:
            self.assertEqual(d.internal_comments,  "")
            self.assertEqual(d.id,                 19971)
            self.assertEqual(d.name,               "draft-ietf-avt-rtp-new")
            self.assertEqual(d.notify,             "magnus.westerlund@ericsson.com, csp@csperkins.org")
            self.assertEqual(d.order,              1)
            self.assertEqual(d.rev,                "12")
            self.assertEqual(d.external_url,       "")
            self.assertEqual(d.expires,            "2003-09-08T00:00:12")
            self.assertEqual(d.type,               DocumentTypeURI("/api/v1/name/doctypename/draft/"))
            self.assertEqual(d.group,              GroupURI("/api/v1/group/group/941/"))
            self.assertEqual(d.resource_uri,       DocumentURI("/api/v1/doc/document/draft-ietf-avt-rtp-new/"))
            self.assertEqual(d.title,              "RTP: A Transport Protocol for Real-Time Applications")
            # self.assertEqual(d.abstract,         "This memorandum describes RTP, the real-time transport protocol...")
            self.assertEqual(d.uploaded_filename,  "")
            self.assertEqual(d.rfc,                3550)
            self.assertEqual(d.shepherd,           None)
            self.assertEqual(d.submissions,        [])
            self.assertEqual(d.intended_std_level, "/api/v1/name/intendedstdlevelname/std/")
            self.assertEqual(d.ad,                 PersonURI("/api/v1/person/person/2515/"))
            self.assertEqual(d.note,               "")
            self.assertEqual(d.words,              34861)
            self.assertEqual(d.tags,               ["/api/v1/name/doctagname/app-min/", "/api/v1/name/doctagname/errata/"])
            self.assertEqual(d.time,               datetime.fromisoformat("2015-10-14T13:49:52"))
            self.assertEqual(d.pages,              104)
            self.assertEqual(d.stream,             StreamURI("/api/v1/name/streamname/ietf/"))
            self.assertEqual(d.std_level,          "/api/v1/name/stdlevelname/std/")
            self.assertEqual(d.states,             [DocumentStateURI("/api/v1/doc/state/3/"), DocumentStateURI("/api/v1/doc/state/7/")])

            url = d.url()
            self.assertEqual(url, "https://www.ietf.org/archive/id/draft-ietf-avt-rtp-new-12.txt")
            self.assertEqual(self.dt.session.get(url).status_code, 200)
        else:
            self.fail("Cannot find document")


    def test_document_liaison(self) -> None:
        d  = self.dt.document(DocumentURI("/api/v1/doc/document/liaison-2012-05-31-3gpp-mmusic-on-rtcp-bandwidth-negotiation-attachment-1/"))
        if d is not None:
            self.assertEqual(d.internal_comments,  "")
            self.assertEqual(d.id,                 46457)
            self.assertEqual(d.name,               "liaison-2012-05-31-3gpp-mmusic-on-rtcp-bandwidth-negotiation-attachment-1")
            self.assertEqual(d.notify,             "")
            self.assertEqual(d.order,              1)
            self.assertEqual(d.rev,                "")
            self.assertEqual(d.external_url,       "")
            self.assertEqual(d.expires,            None)
            self.assertEqual(d.type,               DocumentTypeURI("/api/v1/name/doctypename/liaison/"))
            self.assertEqual(d.group,              None)
            self.assertEqual(d.resource_uri,       DocumentURI("/api/v1/doc/document/liaison-2012-05-31-3gpp-mmusic-on-rtcp-bandwidth-negotiation-attachment-1/"))
            self.assertEqual(d.title,              "S4-120810 DRAFT LS to IETF MMUSIC WG on RTCP Bandwidth Negotiation")
            self.assertEqual(d.abstract,           "")
            self.assertEqual(d.uploaded_filename,  "liaison-2012-05-31-3gpp-mmusic-on-rtcp-bandwidth-negotiation-attachment-1.doc")
            self.assertEqual(d.rfc,                None)
            self.assertEqual(d.shepherd,           None)
            self.assertEqual(d.submissions,        [])
            self.assertEqual(d.intended_std_level, None)
            self.assertEqual(d.ad,                 None)
            self.assertEqual(d.note,               "")
            self.assertEqual(d.words,              None)
            self.assertEqual(d.tags,               [])
            self.assertEqual(d.time,               datetime.fromisoformat("2012-06-04T08:20:38"))
            self.assertEqual(d.pages,              None)
            self.assertEqual(d.stream,             None)
            self.assertEqual(d.std_level,          None)
            self.assertEqual(d.states,             [])

            url = d.url()
            self.assertEqual(url, "https://www.ietf.org/lib/dt/documents/LIAISON/liaison-2012-05-31-3gpp-mmusic-on-rtcp-bandwidth-negotiation-attachment-1.doc")
            self.assertEqual(self.dt.session.get(url).status_code, 200)
        else:
            self.fail("Cannot find document")


    def test_document_liai_att(self) -> None:
        d  = self.dt.document(DocumentURI("/api/v1/doc/document/liaison-2004-08-23-itu-t-ietf-liaison-statement-to-ietf-and-itu-t-study-groups-countering-spam-pdf-version-attachment-1/"))
        if d is not None:
            self.assertEqual(d.internal_comments,  "")
            self.assertEqual(d.id,                 43519)
            self.assertEqual(d.name,               "liaison-2004-08-23-itu-t-ietf-liaison-statement-to-ietf-and-itu-t-study-groups-countering-spam-pdf-version-attachment-1")
            self.assertEqual(d.notify,             "")
            self.assertEqual(d.order,              1)
            self.assertEqual(d.rev,                "")
            self.assertEqual(d.external_url,       "")
            self.assertEqual(d.expires,            None)
            self.assertEqual(d.type,               DocumentTypeURI("/api/v1/name/doctypename/liai-att/"))
            self.assertEqual(d.group,              None)
            self.assertEqual(d.resource_uri,       DocumentURI("/api/v1/doc/document/liaison-2004-08-23-itu-t-ietf-liaison-statement-to-ietf-and-itu-t-study-groups-countering-spam-pdf-version-attachment-1/"))
            self.assertEqual(d.title,              "Liaison Statement to IETF and ITU-T Study Groups: Countering SPAM (PDF version)")
            self.assertEqual(d.abstract,           "")
            self.assertEqual(d.uploaded_filename,  "file39.pdf")
            self.assertEqual(d.rfc,                None)
            self.assertEqual(d.shepherd,           None)
            self.assertEqual(d.submissions,        [])
            self.assertEqual(d.intended_std_level, None)
            self.assertEqual(d.ad,                 None)
            self.assertEqual(d.note,               "")
            self.assertEqual(d.words,              None)
            self.assertEqual(d.tags,               [])
            self.assertEqual(d.time,               datetime.fromisoformat("2004-08-23T00:00:00"))
            self.assertEqual(d.pages,              None)
            self.assertEqual(d.stream,             None)
            self.assertEqual(d.std_level,          None)
            self.assertEqual(d.states,             [])

            url = d.url()
            self.assertEqual(url, "https://www.ietf.org/lib/dt/documents/LIAISON/file39.pdf")
            self.assertEqual(self.dt.session.get(url).status_code, 200)
        else:
            self.fail("Cannot find document")


    def test_document_minutes(self) -> None:
        d  = self.dt.document(DocumentURI("/api/v1/doc/document/minutes-89-cfrg/"))
        if d is not None:
            self.assertEqual(d.internal_comments,  "")
            self.assertEqual(d.id,                 272)
            self.assertEqual(d.name,               "minutes-89-cfrg")
            self.assertEqual(d.notify,             "")
            self.assertEqual(d.order,              1)
            self.assertEqual(d.rev,                "1")
            self.assertEqual(d.external_url,       "")
            self.assertEqual(d.expires,            None)
            self.assertEqual(d.type,               DocumentTypeURI("/api/v1/name/doctypename/minutes/"))
            self.assertEqual(d.group,              GroupURI("/api/v1/group/group/31/"))
            self.assertEqual(d.resource_uri,       DocumentURI("/api/v1/doc/document/minutes-89-cfrg/"))
            self.assertEqual(d.title,              "Minutes for CFRG at IETF-89")
            self.assertEqual(d.abstract,           "")
            self.assertEqual(d.uploaded_filename,  "minutes-89-cfrg.txt")
            self.assertEqual(d.rfc,                None)
            self.assertEqual(d.shepherd,           None)
            self.assertEqual(d.submissions,        [])
            self.assertEqual(d.intended_std_level, None)
            self.assertEqual(d.ad,                 None)
            self.assertEqual(d.note,               "")
            self.assertEqual(d.words,              None)
            self.assertEqual(d.tags,               [])
            self.assertEqual(d.time,               datetime.fromisoformat("2014-04-09T08:09:14"))
            self.assertEqual(d.pages,              None)
            self.assertEqual(d.stream,             None)
            self.assertEqual(d.std_level,          None)
            self.assertEqual(d.states,             [DocumentStateURI("/api/v1/doc/state/79/")])

            url = d.url()
            self.assertEqual(url, "https://datatracker.ietf.org/meeting/89/materials/minutes-89-cfrg.txt")
            self.assertEqual(self.dt.session.get(url).status_code, 200)
        else:
            self.fail("Cannot find document")


    def test_document_recording(self) -> None:
        d  = self.dt.document(DocumentURI("/api/v1/doc/document/recording-94-taps-1/"))
        if d is not None:
            self.assertEqual(d.internal_comments,  "")
            self.assertEqual(d.id,                 49624)
            self.assertEqual(d.name,               "recording-94-taps-1")
            self.assertEqual(d.notify,             "")
            self.assertEqual(d.order,              1)
            self.assertEqual(d.rev,                "00")
            self.assertEqual(d.external_url,       "https://www.ietf.org/audio/ietf94/ietf94-room304-20151103-1520.mp3")
            self.assertEqual(d.expires,            None)
            self.assertEqual(d.type,               DocumentTypeURI("/api/v1/name/doctypename/recording/"))
            self.assertEqual(d.group,              GroupURI("/api/v1/group/group/1924/"))
            self.assertEqual(d.resource_uri,       DocumentURI("/api/v1/doc/document/recording-94-taps-1/"))
            self.assertEqual(d.title,              "Audio recording for 2015-11-03 15:20")
            self.assertEqual(d.abstract,           "")
            self.assertEqual(d.uploaded_filename,  "")
            self.assertEqual(d.rfc,                None)
            self.assertEqual(d.shepherd,           None)
            self.assertEqual(d.submissions,        [])
            self.assertEqual(d.intended_std_level, None)
            self.assertEqual(d.ad,                 None)
            self.assertEqual(d.note,               "")
            self.assertEqual(d.words,              None)
            self.assertEqual(d.tags,               [])
            self.assertEqual(d.time,               datetime.fromisoformat("2015-11-24T08:23:42"))
            self.assertEqual(d.pages,              None)
            self.assertEqual(d.stream,             None)
            self.assertEqual(d.std_level,          None)
            self.assertEqual(d.states,             [DocumentStateURI("/api/v1/doc/state/135/")])

            url = d.url()
            self.assertEqual(url, "https://www.ietf.org/audio/ietf94/ietf94-room304-20151103-1520.mp3")
            # Downloading the MP3 is expensive, so check a HEAD request instead:
            self.assertEqual(self.dt.session.head(url).status_code, 200)
        else:
            self.fail("Cannot find document")


    def test_document_review(self) -> None:
        d  = self.dt.document(DocumentURI("/api/v1/doc/document/review-bchv-rfc6890bis-04-genart-lc-kyzivat-2017-02-28/"))
        if d is not None:
            self.assertEqual(d.internal_comments,  "")
            self.assertEqual(d.id,                 69082)
            self.assertEqual(d.name,               "review-bchv-rfc6890bis-04-genart-lc-kyzivat-2017-02-28")
            self.assertEqual(d.notify,             "")
            self.assertEqual(d.order,              1)
            self.assertEqual(d.rev,                "00")
            self.assertEqual(d.external_url,       "")
            self.assertEqual(d.expires,            None)
            self.assertEqual(d.type,               DocumentTypeURI("/api/v1/name/doctypename/review/"))
            self.assertEqual(d.group,              GroupURI("/api/v1/group/group/1972/"))
            self.assertEqual(d.resource_uri,       DocumentURI("/api/v1/doc/document/review-bchv-rfc6890bis-04-genart-lc-kyzivat-2017-02-28/"))
            self.assertEqual(d.title,              "Last Call Review of draft-bchv-rfc6890bis-04")
            self.assertEqual(d.abstract,           "")
            self.assertEqual(d.uploaded_filename,  "")
            self.assertEqual(d.rfc,                None)
            self.assertEqual(d.shepherd,           None)
            self.assertEqual(d.submissions,        [])
            self.assertEqual(d.intended_std_level, None)
            self.assertEqual(d.ad,                 None)
            self.assertEqual(d.note,               "")
            self.assertEqual(d.words,              None)
            self.assertEqual(d.tags,               [])
            self.assertEqual(d.time,               datetime.fromisoformat("2017-02-28T12:52:33"))
            self.assertEqual(d.pages,              None)
            self.assertEqual(d.stream,             None)
            self.assertEqual(d.std_level,          None)
            self.assertEqual(d.states,             [DocumentStateURI("/api/v1/doc/state/143/")])

            url = d.url()
            self.assertEqual(url, "https://datatracker.ietf.org/doc/review-bchv-rfc6890bis-04-genart-lc-kyzivat-2017-02-28")
            self.assertEqual(self.dt.session.get(url).status_code, 200)
        else:
            self.fail("Cannot find document")


    def test_document_shepwrit(self) -> None:
        for d in self.dt.documents(doctype=self.dt.document_type("shepwrit")):
            self.fail("shepwrit is not used, so this should return no documents")


    def test_document_slides(self) -> None:
        d  = self.dt.document(DocumentURI("/api/v1/doc/document/slides-65-l2vpn-4/"))
        if d is not None:
            self.assertEqual(d.internal_comments,  "")
            self.assertEqual(d.id,                 736)
            self.assertEqual(d.name,               "slides-65-l2vpn-4")
            self.assertEqual(d.notify,             "")
            self.assertEqual(d.order,              4)
            self.assertEqual(d.rev,                "00")
            self.assertEqual(d.external_url,       "")
            self.assertEqual(d.expires,            None)
            self.assertEqual(d.type,               DocumentTypeURI("/api/v1/name/doctypename/slides/"))
            self.assertEqual(d.group,              GroupURI("/api/v1/group/group/1593/"))
            self.assertEqual(d.resource_uri,       DocumentURI("/api/v1/doc/document/slides-65-l2vpn-4/"))
            self.assertEqual(d.title,              "Congruency for VPLS Mcast & Unicast Paths")
            self.assertEqual(d.abstract,           "")
            self.assertEqual(d.uploaded_filename,  "l2vpn-4.pdf")
            self.assertEqual(d.rfc,                None)
            self.assertEqual(d.shepherd,           None)
            self.assertEqual(d.submissions,        [])
            self.assertEqual(d.intended_std_level, None)
            self.assertEqual(d.ad,                 None)
            self.assertEqual(d.note,               "")
            self.assertEqual(d.words,              None)
            self.assertEqual(d.tags,               [])
            self.assertEqual(d.time,               datetime.fromisoformat("2006-04-07T17:30:22"))
            self.assertEqual(d.pages,              None)
            self.assertEqual(d.stream,             None)
            self.assertEqual(d.std_level,          None)
            self.assertEqual(d.states,             [DocumentStateURI("/api/v1/doc/state/141/"), DocumentStateURI("/api/v1/doc/state/138/")])

            url = d.url()
            self.assertEqual(url, "https://www.ietf.org/proceedings/65/slides/l2vpn-4.pdf")
            self.assertEqual(self.dt.session.get(url).status_code, 200)
        else:
            self.fail("Cannot find document")


    def test_document_statchg(self) -> None:
        d  = self.dt.document(DocumentURI("/api/v1/doc/document/status-change-rfc3044-rfc3187-orig-urn-regs-to-historic/"))
        if d is not None:
            self.assertEqual(d.internal_comments,  "")
            self.assertEqual(d.id,                 78306)
            self.assertEqual(d.name,               "status-change-rfc3044-rfc3187-orig-urn-regs-to-historic")
            self.assertEqual(d.notify,             "")
            self.assertEqual(d.order,              1)
            self.assertEqual(d.rev,                "00")
            self.assertEqual(d.external_url,       "")
            self.assertEqual(d.expires,            None)
            self.assertEqual(d.type,               DocumentTypeURI("/api/v1/name/doctypename/statchg/"))
            self.assertEqual(d.group,              GroupURI("/api/v1/group/group/2/"))
            self.assertEqual(d.resource_uri,       DocumentURI("/api/v1/doc/document/status-change-rfc3044-rfc3187-orig-urn-regs-to-historic/"))
            self.assertEqual(d.title,              "Change status of RFC 3044 and RFC 3187 (original ISSN and ISBN URN Namespace registrationS) to Historic")
            self.assertEqual(d.abstract,           "")
            self.assertEqual(d.uploaded_filename,  "")
            self.assertEqual(d.rfc,                None)
            self.assertEqual(d.shepherd,           None)
            self.assertEqual(d.submissions,        [])
            self.assertEqual(d.intended_std_level, None)
            self.assertEqual(d.ad,                 PersonURI("/api/v1/person/person/102154/"))
            self.assertEqual(d.note,               "")
            self.assertEqual(d.words,              None)
            self.assertEqual(d.tags,               [])
            self.assertEqual(d.time,               datetime.fromisoformat("2017-08-21T09:32:46"))
            self.assertEqual(d.pages,              None)
            self.assertEqual(d.stream,             StreamURI("/api/v1/name/streamname/ietf/"))
            self.assertEqual(d.std_level,          None)
            self.assertEqual(d.states,             [DocumentStateURI("/api/v1/doc/state/127/")])

            url = d.url()
            self.assertEqual(url, "https://www.ietf.org/sc/status-change-rfc3044-rfc3187-orig-urn-regs-to-historic-00.txt")
            self.assertEqual(self.dt.session.get(url).status_code, 200)
        else:
            self.fail("Cannot find document")


    def test_documents(self):
        documents = list(self.dt.documents(doctype=self.dt.document_type("draft"), group=self.dt.group_from_acronym("xrblock")))
        self.assertEqual(len(documents), 21)
        self.assertEqual(len([x for x in documents if x.name == "draft-ietf-xrblock-rtcp-xr-discard-rle-metrics"]), 1)
        self.assertEqual(len([x for x in documents if x.name == "draft-ietf-xrblock-rtcp-xr-pdv"]), 1)
        self.assertEqual(len([x for x in documents if x.name == "draft-ietf-xrblock-rtcp-xr-meas-identity"]), 1)
        self.assertEqual(len([x for x in documents if x.name == "draft-ietf-xrblock-rtcp-xr-delay"]), 1)
        self.assertEqual(len([x for x in documents if x.name == "draft-ietf-xrblock-rtcp-xr-burst-gap-loss"]), 1)
        self.assertEqual(len([x for x in documents if x.name == "draft-ietf-xrblock-rtcp-xr-burst-gap-discard"]), 1)
        self.assertEqual(len([x for x in documents if x.name == "draft-ietf-xrblock-rtcp-xr-discard"]), 1)
        self.assertEqual(len([x for x in documents if x.name == "draft-ietf-xrblock-rtcp-xr-qoe"]), 1)
        self.assertEqual(len([x for x in documents if x.name == "draft-ietf-xrblock-rtcp-xr-jb"]), 1)
        self.assertEqual(len([x for x in documents if x.name == "draft-ietf-xrblock-rtcp-xr-loss-conceal"]), 1)
        self.assertEqual(len([x for x in documents if x.name == "draft-ietf-xrblock-rtcp-xr-concsec"]), 1)
        self.assertEqual(len([x for x in documents if x.name == "draft-ietf-xrblock-rtcp-xr-synchronization"]), 1)
        self.assertEqual(len([x for x in documents if x.name == "draft-ietf-xrblock-rtcp-xr-summary-stat"]), 1)
        self.assertEqual(len([x for x in documents if x.name == "draft-ietf-xrblock-rtcp-xr-decodability"]), 1)
        self.assertEqual(len([x for x in documents if x.name == "draft-ietf-xrblock-rtcp-xr-bytes-discarded-metric"]), 1)
        self.assertEqual(len([x for x in documents if x.name == "draft-ietf-xrblock-rtcp-xt-discard-metrics"]), 1)
        self.assertEqual(len([x for x in documents if x.name == "draft-ietf-xrblock-rtcp-xr-post-repair-loss-count"]), 1)
        self.assertEqual(len([x for x in documents if x.name == "draft-ietf-xrblock-rtcp-xr-psi-decodability"]), 1)
        self.assertEqual(len([x for x in documents if x.name == "draft-ietf-xrblock-rtcweb-rtcp-xr-metrics"]), 1)
        self.assertEqual(len([x for x in documents if x.name == "draft-ietf-xrblock-rtcp-xr-video-lc"]), 1)
        self.assertEqual(len([x for x in documents if x.name == "draft-ietf-xrblock-independent-burst-gap-discard"]), 1)


    # FIXME: this needs to be updated
    def test_document_from_draft(self) -> None:
        d  = self.dt.document_from_draft("draft-ietf-avt-rtp-new")
        if d is not None:
            self.assertEqual(d.resource_uri, DocumentURI("/api/v1/doc/document/draft-ietf-avt-rtp-new/"))
        else:
            self.fail("Cannot find document")

    # FIXME: this needs to be updated
    def test_document_from_rfc(self) -> None:
        d  = self.dt.document_from_rfc("rfc3550")
        if d is not None:
            self.assertEqual(d.resource_uri, DocumentURI("/api/v1/doc/document/draft-ietf-avt-rtp-new/"))
        else:
            self.fail("Cannot find document")

    # FIXME: this needs to be updated
    def test_documents_from_bcp(self) -> None:
        d  = list(self.dt.documents_from_bcp("bcp205"))
        if d is not None:
            self.assertEqual(len(d), 1)
            self.assertEqual(d[0].resource_uri, DocumentURI("/api/v1/doc/document/draft-sheffer-rfc6982bis/"))
        else:
            self.fail("Cannot find document")

    # FIXME: this needs to be updated
    def test_documents_from_std(self) -> None:
        d  = list(self.dt.documents_from_std("std68"))
        self.assertEqual(len(d), 1)
        self.assertEqual(d[0].resource_uri, DocumentURI("/api/v1/doc/document/draft-crocker-rfc4234bis/"))


    def test_document_state(self) -> None:
        s = self.dt.document_state(DocumentStateURI('/api/v1/doc/state/7/'))
        if s is not None:
            self.assertEqual(s.id,           7)
            self.assertEqual(s.resource_uri, DocumentStateURI("/api/v1/doc/state/7/"))
            self.assertEqual(s.name,         "RFC Published")
            self.assertEqual(s.desc,         "The ID has been published as an RFC.")
            self.assertEqual(s.type,         DocumentStateTypeURI("/api/v1/doc/statetype/draft-iesg/"))
            self.assertEqual(s.next_states,  [DocumentStateURI("/api/v1/doc/state/8/")])
            self.assertEqual(s.order,        32)
            self.assertEqual(s.slug,         "pub")
            self.assertEqual(s.used,         True)
        else:
            self.fail("Cannot find state")


    def test_document_states(self) -> None:
        st = self.dt.document_state_type(DocumentStateTypeURI("/api/v1/doc/statetype/draft-rfceditor/"))
        states = list(self.dt.document_states(state_type = st))
        self.assertEqual(len(states), 15)
        self.assertEqual(len([x for x in states if x.slug == "auth"]), 1)
        self.assertEqual(len([x for x in states if x.slug == "auth48"]), 1)
        self.assertEqual(len([x for x in states if x.slug == "iana"]), 1)
        self.assertEqual(len([x for x in states if x.slug == "isr"]), 1)
        self.assertEqual(len([x for x in states if x.slug == "ref"]), 1)
        self.assertEqual(len([x for x in states if x.slug == "rfc-edit"]), 1)
        self.assertEqual(len([x for x in states if x.slug == "timeout"]), 1)
        self.assertEqual(len([x for x in states if x.slug == "missref"]), 1)
        self.assertEqual(len([x for x in states if x.slug == "auth48-done"]), 1)
        self.assertEqual(len([x for x in states if x.slug == "edit"]), 1)
        self.assertEqual(len([x for x in states if x.slug == "iana-crd"]), 1)
        self.assertEqual(len([x for x in states if x.slug == "iesg"]), 1)
        self.assertEqual(len([x for x in states if x.slug == "isr-auth"]), 1)
        self.assertEqual(len([x for x in states if x.slug == "pending"]), 1)
        self.assertEqual(len([x for x in states if x.slug == "tooling-issue"]), 1)


    def test_document_state_type(self) -> None:
        st = self.dt.document_state_type(DocumentStateTypeURI("/api/v1/doc/statetype/draft-rfceditor/"))
        if st is not None:
            self.assertEqual(st.resource_uri, DocumentStateTypeURI("/api/v1/doc/statetype/draft-rfceditor/"))
            self.assertEqual(st.slug,  "draft-rfceditor")
            self.assertEqual(st.label, "RFC Editor state")
        else:
            self.fail("Cannot find state type")


    def test_document_state_types(self) -> None:
        st = list(self.dt.document_state_types())
        self.assertEqual(len(st), 24)
        self.assertEqual(len([x for x in st if x.slug == 'draft']), 1)
        self.assertEqual(len([x for x in st if x.slug == 'draft-iesg']), 1)
        self.assertEqual(len([x for x in st if x.slug == 'draft-iana']), 1)
        self.assertEqual(len([x for x in st if x.slug == 'draft-rfceditor']), 1)
        self.assertEqual(len([x for x in st if x.slug == 'draft-stream-ietf']), 1)
        self.assertEqual(len([x for x in st if x.slug == 'draft-stream-irtf']), 1)
        self.assertEqual(len([x for x in st if x.slug == 'draft-stream-ise']), 1)
        self.assertEqual(len([x for x in st if x.slug == 'draft-stream-iab']), 1)
        self.assertEqual(len([x for x in st if x.slug == 'slides']), 1)
        self.assertEqual(len([x for x in st if x.slug == 'minutes']), 1)
        self.assertEqual(len([x for x in st if x.slug == 'agenda']), 1)
        self.assertEqual(len([x for x in st if x.slug == 'liai-att']), 1)
        self.assertEqual(len([x for x in st if x.slug == 'charter']), 1)
        self.assertEqual(len([x for x in st if x.slug == 'conflrev']), 1)
        self.assertEqual(len([x for x in st if x.slug == 'draft-iana-action']), 1)
        self.assertEqual(len([x for x in st if x.slug == 'draft-iana-review']), 1)
        self.assertEqual(len([x for x in st if x.slug == 'statchg']), 1)
        self.assertEqual(len([x for x in st if x.slug == 'recording']), 1)
        self.assertEqual(len([x for x in st if x.slug == 'bluesheets']), 1)
        self.assertEqual(len([x for x in st if x.slug == 'reuse_policy']), 1)
        self.assertEqual(len([x for x in st if x.slug == 'review']), 1)
        self.assertEqual(len([x for x in st if x.slug == 'liaison']), 1)
        self.assertEqual(len([x for x in st if x.slug == 'shepwrit']), 1)
        self.assertEqual(len([x for x in st if x.slug == 'draft-iana-experts']), 1)


    def test_document_event(self) -> None:
        e = self.dt.document_event(DocumentEventURI("/api/v1/doc/docevent/729040/"))
        if e is not None:
            self.assertEqual(e.id,              729040)
            self.assertEqual(e.resource_uri,    DocumentEventURI("/api/v1/doc/docevent/729040/"))
            self.assertEqual(e.by,              PersonURI("/api/v1/person/person/121595/"))
            self.assertEqual(e.doc,             DocumentURI("/api/v1/doc/document/draft-irtf-cfrg-randomness-improvements/"))
            self.assertEqual(e.type,            "new_revision")
            self.assertEqual(e.desc,            "New version available: <b>draft-irtf-cfrg-randomness-improvements-09.txt</b>")
            self.assertEqual(e.rev,             "09")
            self.assertEqual(e.time,            datetime.fromisoformat("2020-01-27T06:41:36"))
        else:
            self.fail("Cannot find event")


    def test_document_events(self) -> None:
        p  = self.dt.person_from_email("csp@csperkins.org")
        d  = self.dt.document_from_draft("draft-ietf-avtcore-rtp-circuit-breakers")
        de = list(self.dt.document_events(doc=d, by=p, event_type="new_revision"))
        self.assertEqual(len(de), 19)
        self.assertEqual(len([x for x in de if x.id == 478637]), 1)
        self.assertEqual(len([x for x in de if x.id == 475709]), 1)
        self.assertEqual(len([x for x in de if x.id == 470372]), 1)
        self.assertEqual(len([x for x in de if x.id == 466353]), 1)
        self.assertEqual(len([x for x in de if x.id == 460235]), 1)
        self.assertEqual(len([x for x in de if x.id == 456912]), 1)
        self.assertEqual(len([x for x in de if x.id == 456736]), 1)
        self.assertEqual(len([x for x in de if x.id == 444539]), 1)
        self.assertEqual(len([x for x in de if x.id == 415925]), 1)
        self.assertEqual(len([x for x in de if x.id == 413197]), 1)
        self.assertEqual(len([x for x in de if x.id == 402942]), 1)
        self.assertEqual(len([x for x in de if x.id == 397776]), 1)
        self.assertEqual(len([x for x in de if x.id == 384673]), 1)
        self.assertEqual(len([x for x in de if x.id == 369306]), 1)
        self.assertEqual(len([x for x in de if x.id == 364835]), 1)
        self.assertEqual(len([x for x in de if x.id == 340119]), 1)
        self.assertEqual(len([x for x in de if x.id == 326064]), 1)
        self.assertEqual(len([x for x in de if x.id == 307226]), 1)
        self.assertEqual(len([x for x in de if x.id == 306017]), 1)


    def test_ballot_position_name(self) -> None:
        bp = self.dt.ballot_position_name(BallotPositionNameURI("/api/v1/name/ballotpositionname/moretime/"))
        if bp is not None:
            self.assertEqual(bp.blocking,     False)
            self.assertEqual(bp.desc,         "")
            self.assertEqual(bp.order,        0)
            self.assertEqual(bp.resource_uri, BallotPositionNameURI("/api/v1/name/ballotpositionname/moretime/"))
            self.assertEqual(bp.slug,         "moretime")
            self.assertEqual(bp.used,         True)


    def test_ballot_position_names(self) -> None:
        bps = list(self.dt.ballot_position_names())
        self.assertEqual(len(bps), 9)
        self.assertEqual(len([x for x in bps if x.slug == "moretime"]), 1)
        self.assertEqual(len([x for x in bps if x.slug == "notready"]), 1)
        self.assertEqual(len([x for x in bps if x.slug ==      "yes"]), 1)
        self.assertEqual(len([x for x in bps if x.slug ==    "noobj"]), 1)
        self.assertEqual(len([x for x in bps if x.slug ==    "block"]), 1)
        self.assertEqual(len([x for x in bps if x.slug ==  "discuss"]), 1)
        self.assertEqual(len([x for x in bps if x.slug ==  "abstain"]), 1)
        self.assertEqual(len([x for x in bps if x.slug ==   "recuse"]), 1)
        self.assertEqual(len([x for x in bps if x.slug == "norecord"]), 1)


    def test_ballot_type(self) -> None:
        bt = self.dt.ballot_type(BallotTypeURI("/api/v1/doc/ballottype/5/"))
        if bt is not None:
            self.assertEqual(bt.doc_type,       DocumentTypeURI("/api/v1/name/doctypename/conflrev/"))
            self.assertEqual(bt.id,             5)
            self.assertEqual(bt.name,           "Approve")
            self.assertEqual(bt.order,          0)
            self.assertEqual(len(bt.positions), 6)
            self.assertEqual(bt.positions[0],   BallotPositionNameURI("/api/v1/name/ballotpositionname/yes/"))
            self.assertEqual(bt.positions[1],   BallotPositionNameURI("/api/v1/name/ballotpositionname/noobj/"))
            self.assertEqual(bt.positions[2],   BallotPositionNameURI("/api/v1/name/ballotpositionname/discuss/"))
            self.assertEqual(bt.positions[3],   BallotPositionNameURI("/api/v1/name/ballotpositionname/abstain/"))
            self.assertEqual(bt.positions[4],   BallotPositionNameURI("/api/v1/name/ballotpositionname/recuse/"))
            self.assertEqual(bt.positions[5],   BallotPositionNameURI("/api/v1/name/ballotpositionname/norecord/"))
            self.assertEqual(bt.question,       "Is this the correct conflict review response?")
            self.assertEqual(bt.resource_uri,   BallotTypeURI("/api/v1/doc/ballottype/5/"))
            self.assertEqual(bt.slug,           "conflrev")
            self.assertEqual(bt.used,           True)
        else:
            self.fail("Could not find ballot type")


    def test_ballot_types_doctype(self) -> None:
        bts = list(self.dt.ballot_types(self.dt.document_type("draft")))
        self.assertEqual(len(bts), 2)
        self.assertEqual(bts[0].slug, "irsg-approve")
        self.assertEqual(bts[1].slug, "approve")


    def test_ballot_document_event(self) -> None:
        e = self.dt.ballot_document_event(BallotDocumentEventURI("/api/v1/doc/ballotdocevent/744784/"))
        if e is not None:
            self.assertEqual(e.ballot_type,  BallotTypeURI("/api/v1/doc/ballottype/5/"))
            self.assertEqual(e.by,           PersonURI("/api/v1/person/person/21684/"))
            self.assertEqual(e.desc,         'Created "Approve" ballot')
            self.assertEqual(e.doc,          DocumentURI("/api/v1/doc/document/conflict-review-dold-payto/"))
            self.assertEqual(e.docevent_ptr, DocumentEventURI("/api/v1/doc/docevent/744784/"))
            self.assertEqual(e.id,           744784)
            self.assertEqual(e.resource_uri, BallotDocumentEventURI("/api/v1/doc/ballotdocevent/744784/"))
            self.assertEqual(e.rev,          "00")
            self.assertEqual(e.time,         datetime.fromisoformat("2020-04-04T10:57:29"))
            self.assertEqual(e.type,         "created_ballot")
        else:
            self.fail("Cannot find ballot event")


    def test_ballot_document_events(self) -> None:
        d  = self.dt.document_from_draft("draft-ietf-avtcore-rtp-circuit-breakers")
        de = list(self.dt.ballot_document_events(doc=d))
        self.assertEqual(len(de), 2)
        self.assertEqual(len([x for x in de if x.id == 478676]), 1)
        self.assertEqual(len([x for x in de if x.id == 461800]), 1)

        bt = self.dt.ballot_type(BallotTypeURI("/api/v1/doc/ballottype/3/")) # Charter approval
        p  = self.dt.person(PersonURI("/api/v1/person/person/108756/"))      # Cindy Morgan
        d  = self.dt.document(DocumentURI("/api/v1/doc/document/charter-ietf-rmcat/"))
        de = list(self.dt.ballot_document_events(doc = d, ballot_type = bt, by = p, event_type = "closed_ballot"))
        self.assertEqual(len(de), 1)
        self.assertEqual(de[0].id, 304166)


    def test_documents_authored_by_person(self) -> None:
        p = self.dt.person_from_email("ladan@isi.edu")
        if p is not None:
            authored = list(self.dt.documents_authored_by_person(p))
            self.assertEqual(len(authored), 7)
            self.assertEqual(len([x for x in authored if x.document == DocumentURI(uri='/api/v1/doc/document/draft-gharai-ac3/')]), 1)
            self.assertEqual(len([x for x in authored if x.document == DocumentURI(uri='/api/v1/doc/document/draft-gharai-hdtv-video/')]), 1)
            self.assertEqual(len([x for x in authored if x.document == DocumentURI(uri='/api/v1/doc/document/draft-ietf-avt-smpte292-video/')]), 1)
            self.assertEqual(len([x for x in authored if x.document == DocumentURI(uri='/api/v1/doc/document/draft-gharai-avt-uncomp-video/')]), 1)
            self.assertEqual(len([x for x in authored if x.document == DocumentURI(uri='/api/v1/doc/document/draft-ietf-avt-uncomp-video/')]), 1)
            self.assertEqual(len([x for x in authored if x.document == DocumentURI(uri='/api/v1/doc/document/draft-gharai-avt-tfrc-profile/')]), 1)
            self.assertEqual(len([x for x in authored if x.document == DocumentURI(uri='/api/v1/doc/document/draft-ietf-avt-tfrc-profile/')]), 1)
        else:
            self.fail("Cannot find person");


    def test_documents_authored_by_email(self) -> None:
        e = self.dt.email(EmailURI("/api/v1/person/email/ladan@isi.edu/"))
        if e is not None:
            authored = list(self.dt.documents_authored_by_email(e))
            self.assertEqual(len(authored), 7)
            self.assertEqual(len([x for x in authored if x.document == DocumentURI(uri='/api/v1/doc/document/draft-gharai-ac3/')]), 1)
            self.assertEqual(len([x for x in authored if x.document == DocumentURI(uri='/api/v1/doc/document/draft-gharai-hdtv-video/')]), 1)
            self.assertEqual(len([x for x in authored if x.document == DocumentURI(uri='/api/v1/doc/document/draft-ietf-avt-smpte292-video/')]), 1)
            self.assertEqual(len([x for x in authored if x.document == DocumentURI(uri='/api/v1/doc/document/draft-gharai-avt-uncomp-video/')]), 1)
            self.assertEqual(len([x for x in authored if x.document == DocumentURI(uri='/api/v1/doc/document/draft-ietf-avt-uncomp-video/')]), 1)
            self.assertEqual(len([x for x in authored if x.document == DocumentURI(uri='/api/v1/doc/document/draft-gharai-avt-tfrc-profile/')]), 1)
            self.assertEqual(len([x for x in authored if x.document == DocumentURI(uri='/api/v1/doc/document/draft-ietf-avt-tfrc-profile/')]), 1)
        else:
            self.fail("Cannot find person");




    # FIXME: this needs to be updated
    def test_submission(self) -> None:
        s  = self.dt.submission(SubmissionURI("/api/v1/submit/submission/2402/"))
        if s is not None:
            #self.assertEqual(s.abstract,        "Internet technical specifications often need to...")
            self.assertEqual(s.access_key,      "f77d08da6da54f3cbecca13d31646be8")
            self.assertEqual(s.auth_key,        "fMm6hur5dJ7gV58x5SE0vkHUoDOrSuSF")
            self.assertEqual(s.authors,         "[{'email': 'dcrocker@bbiw.net', 'name': 'Dave Crocker'}, {'email': 'paul.overell@thus.net', 'name': 'Paul Overell'}]")
            self.assertEqual(s.checks,          [SubmissionCheckURI("/api/v1/submit/submissioncheck/386/")])
            self.assertEqual(s.document_date,   "2007-10-09")
            self.assertEqual(s.draft,           DocumentURI("/api/v1/doc/document/draft-crocker-rfc4234bis/"))
            self.assertEqual(s.file_size,       27651)
            self.assertEqual(s.file_types,      ".txt,.xml,.pdf")
            #self.assertEqual(s.first_two_pages, "\n\n\nNetwork Working Group...")
            self.assertEqual(s.group,           GroupURI("/api/v1/group/group/1027/"))
            self.assertEqual(s.id,              2402)
            self.assertEqual(s.name,            "draft-crocker-rfc4234bis")
            self.assertEqual(s.note,            "")
            self.assertEqual(s.pages,           13)
            self.assertEqual(s.remote_ip,       "72.255.3.179")
            self.assertEqual(s.replaces,        "")
            self.assertEqual(s.resource_uri,    SubmissionURI("/api/v1/submit/submission/2402/"))
            self.assertEqual(s.rev,             "01")
            self.assertEqual(s.state,           "/api/v1/name/draftsubmissionstatename/posted/")
            self.assertEqual(s.submission_date, "2007-10-09")
            self.assertEqual(s.submitter,       "Dave Crocker")
            self.assertEqual(s.title,           "Augmented BNF for Syntax Specifications: ABNF")
            self.assertEqual(s.words,           None)
        else:
            self.fail("Cannot find submission")


    def test_submission_event(self) -> None:
        e  = self.dt.submission_event(SubmissionEventURI("/api/v1/submit/submissionevent/188542/"))
        if e is not None:
            self.assertEqual(e.by,           PersonURI("/api/v1/person/person/115824/"))
            self.assertEqual(e.desc,         "Uploaded submission")
            self.assertEqual(e.id,           188542)
            self.assertEqual(e.resource_uri, SubmissionEventURI("/api/v1/submit/submissionevent/188542/"))
            self.assertEqual(e.submission,   SubmissionURI("/api/v1/submit/submission/111128/"))
            self.assertEqual(e.time,         datetime.fromisoformat("2020-03-23T04:18:27"))
        else:
            self.fail("Cannot find submission event")


    def test_document_type(self) -> None:
        doctype = self.dt.document_type("draft")
        if doctype is not None:
            self.assertEqual(doctype.resource_uri, DocumentTypeURI("/api/v1/name/doctypename/draft/"))
            self.assertEqual(doctype.name,         "Draft")
            self.assertEqual(doctype.used,         True)
            self.assertEqual(doctype.prefix,       "draft")
            self.assertEqual(doctype.slug,         "draft")
            self.assertEqual(doctype.desc,         "")
            self.assertEqual(doctype.order,        0)
        else:
            self.fail("Cannot find doctype")


    def test_document_types(self) -> None:
        types = list(self.dt.document_types())
        self.assertEqual(len(types), 13)
        self.assertEqual(len([x for x in types if x.slug == "agenda"]), 1)
        self.assertEqual(len([x for x in types if x.slug == "bluesheets"]), 1)
        self.assertEqual(len([x for x in types if x.slug == "charter"]), 1)
        self.assertEqual(len([x for x in types if x.slug == "conflrev"]), 1)
        self.assertEqual(len([x for x in types if x.slug == "draft"]), 1)
        self.assertEqual(len([x for x in types if x.slug == "liaison"]), 1)
        self.assertEqual(len([x for x in types if x.slug == "liai-att"]), 1)
        self.assertEqual(len([x for x in types if x.slug == "minutes"]), 1)
        self.assertEqual(len([x for x in types if x.slug == "recording"]), 1)
        self.assertEqual(len([x for x in types if x.slug == "review"]), 1)
        self.assertEqual(len([x for x in types if x.slug == "shepwrit"]), 1)
        self.assertEqual(len([x for x in types if x.slug == "slides"]), 1)
        self.assertEqual(len([x for x in types if x.slug == "statchg"]), 1)

    # -----------------------------------------------------------------------------------------------------------------------------
    # Tests relating to streams:

    # FIXME: this needs to be updated
    def test_stream(self) -> None:
        stream = self.dt.stream(StreamURI("/api/v1/name/streamname/irtf/"))
        if stream is not None:
            self.assertEqual(stream.desc,         "IRTF Stream")
            self.assertEqual(stream.name,         "IRTF")
            self.assertEqual(stream.order,        3)
            self.assertEqual(stream.resource_uri, StreamURI("/api/v1/name/streamname/irtf/"))
            self.assertEqual(stream.slug,         "irtf")
            self.assertEqual(stream.used,         True)
        else:
            self.fail("Cannot find stream")

    def test_streams(self) -> None:
        streams = list(self.dt.streams())
        self.assertEqual(len(streams), 5)
        self.assertEqual(len([x for x in streams if x.slug ==   "ietf"]), 1)
        self.assertEqual(len([x for x in streams if x.slug ==   "irtf"]), 1)
        self.assertEqual(len([x for x in streams if x.slug ==    "iab"]), 1)
        self.assertEqual(len([x for x in streams if x.slug ==    "ise"]), 1)
        self.assertEqual(len([x for x in streams if x.slug == "legacy"]), 1)

    # -----------------------------------------------------------------------------------------------------------------------------
    # Tests relating to groups:

    # FIXME: this needs to be updated
    def test_group(self) -> None:
        group = self.dt.group(GroupURI("/api/v1/group/group/941/"))
        if group is not None:
            self.assertEqual(group.acronym,        "avt")
            self.assertEqual(group.ad,             None)
            self.assertEqual(group.charter,        DocumentURI("/api/v1/doc/document/charter-ietf-avt/"))
            self.assertEqual(group.comments,       "")
            self.assertEqual(group.description,    "\n  The Audio/Video Transport Working Group was formed to specify a protocol \n  for real-time transmission of audio and video over unicast and multicast \n  UDP/IP. This is the Real-time Transport Protocol, RTP, along with its \n  associated profiles and payload formats.")
            self.assertEqual(group.id,             941)
            self.assertEqual(group.list_archive,   "https://mailarchive.ietf.org/arch/search/?email_list=avt")
            self.assertEqual(group.list_email,     "avt@ietf.org")
            self.assertEqual(group.list_subscribe, "https://www.ietf.org/mailman/listinfo/avt")
            self.assertEqual(group.name,           "Audio/Video Transport")
            self.assertEqual(group.parent,         GroupURI("/api/v1/group/group/1683/"))
            self.assertEqual(group.resource_uri,   GroupURI("/api/v1/group/group/941/"))
            self.assertEqual(group.state,          GroupStateURI("/api/v1/name/groupstatename/conclude/"))
            self.assertEqual(group.time,           datetime.fromisoformat("2011-12-09T12:00:00"))
            self.assertEqual(group.type,           "/api/v1/name/grouptypename/wg/")
            self.assertEqual(group.unused_states,  [])
            self.assertEqual(group.unused_tags,    [])
        else:
            self.fail("Cannot find group")


    def test_group_from_acronym(self) -> None:
        group = self.dt.group_from_acronym("avt")
        if group is not None:
            self.assertEqual(group.id, 941)
        else:
            self.fail("Cannot find group")
            

    def test_group_from_acronym_invalid(self) -> None:
        group = self.dt.group_from_acronym("invalid")
        self.assertIsNone(group)


    def test_groups(self) -> None:
        groups = self.dt.groups()
        self.assertIsNot(groups, None)
        

    def test_groups_namecontains(self) -> None:
        groups = list(self.dt.groups(name_contains="IRTF"))
        self.assertEqual(len(groups), 2)
        self.assertEqual(len([x for x in groups if x.id ==    3]), 1)
        self.assertEqual(len([x for x in groups if x.id == 1853]), 1)

        
    def test_groups_state(self) -> None:
        groups = list(self.dt.groups(state=self.dt.group_state("abandon")))
        self.assertEqual(len(groups), 6)
        self.assertEqual(len([x for x in groups if x.id == 1949]), 1)
        self.assertEqual(len([x for x in groups if x.id == 2009]), 1)
        self.assertEqual(len([x for x in groups if x.id == 2018]), 1)
        self.assertEqual(len([x for x in groups if x.id == 2155]), 1)
        self.assertEqual(len([x for x in groups if x.id == 2190]), 1)
        self.assertEqual(len([x for x in groups if x.id == 2200]), 1)


    def test_groups_parent(self) -> None:
        groups = list(self.dt.groups(parent=self.dt.group(GroupURI("/api/v1/group/group/1/"))))
        self.assertEqual(len(groups), 2)
        self.assertEqual(len([x for x in groups if x.id ==    2]), 1)
        self.assertEqual(len([x for x in groups if x.id == 2225]), 1)


    def test_group_state(self) -> None:
        state = self.dt.group_state("abandon")
        if state is not None:
            self.assertEqual(state.desc,         "Formation of the group (most likely a BoF or Proposed WG) was abandoned")
            self.assertEqual(state.name,         "Abandoned")
            self.assertEqual(state.order,        0)
            self.assertEqual(state.resource_uri, GroupStateURI("/api/v1/name/groupstatename/abandon/"))
            self.assertEqual(state.slug,         "abandon")
            self.assertEqual(state.used,         True)
        else:
            self.fail("Cannot find group state")


    def test_group_states(self) -> None:
        states = list(self.dt.group_states())
        self.assertEqual(len(states),  9)
        self.assertEqual(len([x for x in states if x.slug == "abandon"]), 1)
        self.assertEqual(len([x for x in states if x.slug == "active"]), 1)
        self.assertEqual(len([x for x in states if x.slug == "bof"]), 1)
        self.assertEqual(len([x for x in states if x.slug == "bof-conc"]), 1)
        self.assertEqual(len([x for x in states if x.slug == "conclude"]), 1)
        self.assertEqual(len([x for x in states if x.slug == "dormant"]), 1)
        self.assertEqual(len([x for x in states if x.slug == "proposed"]), 1)
        self.assertEqual(len([x for x in states if x.slug == "replaced"]), 1)
        self.assertEqual(len([x for x in states if x.slug == "unknown"]), 1)


    # -----------------------------------------------------------------------------------------------------------------------------
    # Tests relating to meetings:

    def test_meeting_schedule(self) -> None:
        schedule = self.dt.meeting_schedule(ScheduleURI("/api/v1/meeting/schedule/209/"))
        if schedule is not None:
            self.assertEqual(schedule.id,           209)
            self.assertEqual(schedule.resource_uri, ScheduleURI("/api/v1/meeting/schedule/209/"))
            self.assertEqual(schedule.meeting,      MeetingURI("/api/v1/meeting/meeting/365/"))
            self.assertEqual(schedule.owner,        PersonURI("/api/v1/person/person/109129/"))
            self.assertEqual(schedule.name,         "prelim-fix")
            self.assertEqual(schedule.visible,      True)
            self.assertEqual(schedule.public,       True)
            self.assertEqual(schedule.badness,      None)
        else:
            self.fail("cannot find meeting schedule")


    def test_meeting_session_assignment(self) -> None:
        assignment = self.dt.meeting_session_assignment(SessionAssignmentURI("/api/v1/meeting/schedtimesessassignment/61212/"))
        if assignment is not None:
            self.assertEqual(assignment.id,           61212)
            self.assertEqual(assignment.modified,     datetime.fromisoformat("2017-10-17T12:14:33"))
            self.assertEqual(assignment.extendedfrom, None)
            self.assertEqual(assignment.timeslot,     TimeslotURI("/api/v1/meeting/timeslot/9132/"))
            self.assertEqual(assignment.session,      SessionURI("/api/v1/meeting/session/25907/"))
            self.assertEqual(assignment.agenda,       ScheduleURI("/api/v1/meeting/schedule/787/"))
            self.assertEqual(assignment.schedule,     ScheduleURI("/api/v1/meeting/schedule/787/"))
            self.assertEqual(assignment.pinned,       False)
            self.assertEqual(assignment.resource_uri, SessionAssignmentURI("/api/v1/meeting/schedtimesessassignment/61212/"))
            self.assertEqual(assignment.badness,      0)
            self.assertEqual(assignment.notes, "")
        else:
            self.fail("cannot find meeting session assignment")


    def test_meeting_session_assignments(self) -> None:
        meeting  = self.dt.meeting(MeetingURI("/api/v1/meeting/meeting/365/")) # IETF 90 in Toronto
        if meeting is not None:
            schedule = self.dt.meeting_schedule(meeting.schedule)
            if schedule is not None:
                assignments = list(self.dt.meeting_session_assignments(schedule))
                self.assertEqual(len(assignments), 161)
            else:
                self.fail("Cannot find schedule")
        else:
            self.fail("Cannot find meeting")


    def test_meeting(self) -> None:
        meeting = self.dt.meeting(MeetingURI("/api/v1/meeting/meeting/365/"))
        if meeting is not None:
            self.assertEqual(meeting.id,                               365)
            self.assertEqual(meeting.resource_uri,                     MeetingURI("/api/v1/meeting/meeting/365/"))
            self.assertEqual(meeting.type,                             MeetingTypeURI("/api/v1/name/meetingtypename/ietf/"))
            self.assertEqual(meeting.city,                             "Toronto")
            self.assertEqual(meeting.country,                          "CA")
            self.assertEqual(meeting.venue_name,                       "Fairmont Royal York Hotel")
            self.assertEqual(meeting.venue_addr,                       "100 Front Street W\r\nToronto, Ontario, Canada M5J 1E3")
            self.assertEqual(meeting.date,                             "2014-07-20")
            self.assertEqual(meeting.days,                             6)
            self.assertEqual(meeting.time_zone,                        "America/Toronto")
            self.assertEqual(meeting.idsubmit_cutoff_day_offset_00,    20)
            self.assertEqual(meeting.idsubmit_cutoff_day_offset_01,    13)
            self.assertEqual(meeting.idsubmit_cutoff_warning_days,     "21 days, 0:00:00")
            self.assertEqual(meeting.idsubmit_cutoff_time_utc,         "23:59:59")
            self.assertEqual(meeting.submission_cutoff_day_offset,     26)
            self.assertEqual(meeting.submission_correction_day_offset, 50)
            self.assertEqual(meeting.submission_start_day_offset,      90)
            self.assertEqual(meeting.attendees,                        1237)
            self.assertEqual(meeting.session_request_lock_message,     "")
            self.assertEqual(meeting.reg_area,                         "Ballroom Foyer ")
            self.assertEqual(meeting.break_area,                       "Convention and Main Mezzanine Level Foyers")
            self.assertEqual(meeting.agenda_info_note,                 "")
            self.assertEqual(meeting.agenda_warning_note,              "")
            self.assertEqual(meeting.show_important_dates,             True)
            self.assertEqual(meeting.updated,                          datetime.fromisoformat("2016-12-22T09:57:15-08:00"))
            self.assertEqual(meeting.agenda,                           ScheduleURI("/api/v1/meeting/schedule/209/"))
            self.assertEqual(meeting.schedule,                         ScheduleURI("/api/v1/meeting/schedule/209/"))
            self.assertEqual(meeting.number,                           "90")
            self.assertEqual(meeting.proceedings_final,                False)
            self.assertEqual(meeting.acknowledgements,                 "")
        else:
            self.fail("Cannot find meeting")


    def test_meetings(self) -> None:
        meetings = list(self.dt.meetings(start_date="2019-01-01", end_date="2019-12-31", meeting_type=self.dt.meeting_type("ietf")))
        self.assertEqual(len(meetings),  3)
        self.assertEqual(len([x for x in meetings if x.city == "Singapore"]), 1)
        self.assertEqual(len([x for x in meetings if x.city ==  "Montreal"]), 1)
        self.assertEqual(len([x for x in meetings if x.city ==    "Prague"]), 1)


    def test_meeting_types(self) -> None:
        types = list(self.dt.meeting_types())
        self.assertEqual(len(types),  2)
        self.assertEqual(types[0].slug, "ietf")
        self.assertEqual(types[1].slug, "interim")


    @patch.object(ietfdata.datatracker, 'datetime', Mock(wraps=datetime))
    def test_meeting_status_future(self) -> None:
        meeting = self.dt.meeting(MeetingURI("/api/v1/meeting/meeting/365/"))
        if meeting is not None:
            ietfdata.datatracker.datetime.now.return_value = datetime(2014, 1, 1) # type: ignore
            self.assertEqual(meeting.status(), MeetingStatus.FUTURE)
        else:
            self.fail("Cannot find meeting")


    @patch.object(ietfdata.datatracker, 'datetime', Mock(wraps=datetime))
    def test_meeting_status_completed(self) -> None:
        meeting = self.dt.meeting(MeetingURI("/api/v1/meeting/meeting/365/"))
        if meeting is not None:
            ietfdata.datatracker.datetime.now.return_value = datetime(2014, 12, 1) # type: ignore
            self.assertEqual(meeting.status(), MeetingStatus.COMPLETED)
        else:
            self.fail("Cannot find meeting")


    @patch.object(ietfdata.datatracker, 'datetime', Mock(wraps=datetime))
    def test_meeting_status_ongoing(self) -> None:
        meeting = self.dt.meeting(MeetingURI("/api/v1/meeting/meeting/365/"))
        if meeting is not None:
            ietfdata.datatracker.datetime.now.return_value = datetime(2014, 7, 20) # type: ignore
            self.assertEqual(meeting.status(), MeetingStatus.ONGOING)
        else:
            self.fail("Cannot find meeting")


    # -----------------------------------------------------------------------------------------------------------------------------
    # Tests relating to related documents:

    def test_related_documents_all(self) -> None:
        source = self.dt.document(DocumentURI("/api/v1/doc/document/draft-rfced-info-snpp-v3/"))
        target = list(self.dt.docaliases_from_name("draft-gwinn-paging-protocol-v3"))[0]
        rel    = self.dt.relationship_type(RelationshipTypeURI("/api/v1/name/docrelationshipname/replaces/"))
        rdocs  = list(self.dt.related_documents(source=source, target=target, relationship_type=rel))
        self.assertEqual(len(rdocs), 1)
        self.assertEqual(rdocs[0].id, 3)
        self.assertEqual(rdocs[0].relationship, RelationshipTypeURI("/api/v1/name/docrelationshipname/replaces/"))
        self.assertEqual(rdocs[0].resource_uri, RelatedDocumentURI("/api/v1/doc/relateddocument/3/"))
        self.assertEqual(rdocs[0].source,       DocumentURI("/api/v1/doc/document/draft-rfced-info-snpp-v3/"))
        self.assertEqual(rdocs[0].target,       DocumentAliasURI("/api/v1/doc/docalias/draft-gwinn-paging-protocol-v3/"))
        

    def test_related_documents_source_target(self) -> None:
        source = self.dt.document(DocumentURI("/api/v1/doc/document/draft-rfced-info-snpp-v3/"))
        target = list(self.dt.docaliases_from_name("draft-gwinn-paging-protocol-v3"))[0]
        rdocs  = list(self.dt.related_documents(source=source, target=target))
        self.assertEqual(len(rdocs), 1)
        self.assertEqual(rdocs[0].id, 3)
        self.assertEqual(rdocs[0].relationship, RelationshipTypeURI("/api/v1/name/docrelationshipname/replaces/"))
        self.assertEqual(rdocs[0].resource_uri, RelatedDocumentURI("/api/v1/doc/relateddocument/3/"))
        self.assertEqual(rdocs[0].source,       DocumentURI("/api/v1/doc/document/draft-rfced-info-snpp-v3/"))
        self.assertEqual(rdocs[0].target,       DocumentAliasURI("/api/v1/doc/docalias/draft-gwinn-paging-protocol-v3/"))


    def test_related_documents_source_relationship(self) -> None:
        source = self.dt.document(DocumentURI("/api/v1/doc/document/draft-rfced-info-snpp-v3/"))
        rel    = self.dt.relationship_type(RelationshipTypeURI("/api/v1/name/docrelationshipname/replaces/"))
        rdocs  = list(self.dt.related_documents(source=source, relationship_type=rel))
        self.assertEqual(len(rdocs), 1)
        self.assertEqual(rdocs[0].id, 3)
        self.assertEqual(rdocs[0].relationship, RelationshipTypeURI("/api/v1/name/docrelationshipname/replaces/"))
        self.assertEqual(rdocs[0].resource_uri, RelatedDocumentURI("/api/v1/doc/relateddocument/3/"))
        self.assertEqual(rdocs[0].source,       DocumentURI("/api/v1/doc/document/draft-rfced-info-snpp-v3/"))
        self.assertEqual(rdocs[0].target,       DocumentAliasURI("/api/v1/doc/docalias/draft-gwinn-paging-protocol-v3/"))


    def test_related_documents_target_relationship(self) -> None:
        target = list(self.dt.docaliases_from_name("draft-gwinn-paging-protocol-v3"))[0]
        rel    = self.dt.relationship_type(RelationshipTypeURI("/api/v1/name/docrelationshipname/replaces/"))
        rdocs  = list(self.dt.related_documents(target=target, relationship_type=rel))
        self.assertEqual(len(rdocs), 1)
        self.assertEqual(rdocs[0].id, 3)
        self.assertEqual(rdocs[0].relationship, RelationshipTypeURI("/api/v1/name/docrelationshipname/replaces/"))
        self.assertEqual(rdocs[0].resource_uri, RelatedDocumentURI("/api/v1/doc/relateddocument/3/"))
        self.assertEqual(rdocs[0].source,       DocumentURI("/api/v1/doc/document/draft-rfced-info-snpp-v3/"))
        self.assertEqual(rdocs[0].target,       DocumentAliasURI("/api/v1/doc/docalias/draft-gwinn-paging-protocol-v3/"))


    def test_related_documents_target(self) -> None:
        target = list(self.dt.docaliases_from_name("draft-gwinn-paging-protocol-v3"))[0]
        rdocs  = list(self.dt.related_documents(target=target))
        self.assertEqual(len(rdocs), 1)
        self.assertEqual(rdocs[0].id, 3)
        self.assertEqual(rdocs[0].relationship, RelationshipTypeURI("/api/v1/name/docrelationshipname/replaces/"))
        self.assertEqual(rdocs[0].resource_uri, RelatedDocumentURI("/api/v1/doc/relateddocument/3/"))
        self.assertEqual(rdocs[0].source,       DocumentURI("/api/v1/doc/document/draft-rfced-info-snpp-v3/"))
        self.assertEqual(rdocs[0].target,       DocumentAliasURI("/api/v1/doc/docalias/draft-gwinn-paging-protocol-v3/"))


    def test_related_documents_source(self) -> None:
        source = self.dt.document(DocumentURI("/api/v1/doc/document/draft-rfced-info-snpp-v3/"))
        rdocs  = list(self.dt.related_documents(source=source))
        self.assertEqual(len(rdocs), 6)
        self.assertEqual(len([x for x in rdocs if x.target == DocumentAliasURI("/api/v1/doc/docalias/draft-gwinn-paging-protocol-v3/")]), 1)
        self.assertEqual(len([x for x in rdocs if x.target == DocumentAliasURI("/api/v1/doc/docalias/rfc1645/")]), 1)
        self.assertEqual(len([x for x in rdocs if x.target == DocumentAliasURI("/api/v1/doc/docalias/rfc1425/")]), 1)
        self.assertEqual(len([x for x in rdocs if x.target == DocumentAliasURI("/api/v1/doc/docalias/rfc1521/")]), 1)
        self.assertEqual(len([x for x in rdocs if x.target == DocumentAliasURI("/api/v1/doc/docalias/std10/")]), 1)
        self.assertEqual(len([x for x in rdocs if x.target == DocumentAliasURI("/api/v1/doc/docalias/rfc1486/")]), 1)


    def test_related_documents_relationship(self) -> None:
        rel    = self.dt.relationship_type(RelationshipTypeURI("/api/v1/name/docrelationshipname/replaces/"))
        rdocs  = self.dt.related_documents(relationship_type=rel)
        self.assertIsNot(rdocs, None)


    def test_relationship_types(self) -> None:
        types = list(self.dt.relationship_types())
        self.assertEqual(len(types), 16)
        self.assertEqual(len([x for x in types if x.slug ==  "downref-approval"]), 1)
        self.assertEqual(len([x for x in types if x.slug ==          "conflrev"]), 1)
        self.assertEqual(len([x for x in types if x.slug ==           "refinfo"]), 1)
        self.assertEqual(len([x for x in types if x.slug ==             "tobcp"]), 1)
        self.assertEqual(len([x for x in types if x.slug ==             "toexp"]), 1)
        self.assertEqual(len([x for x in types if x.slug ==            "tohist"]), 1)
        self.assertEqual(len([x for x in types if x.slug ==             "toinf"]), 1)
        self.assertEqual(len([x for x in types if x.slug ==              "tois"]), 1)
        self.assertEqual(len([x for x in types if x.slug ==              "tops"]), 1)
        self.assertEqual(len([x for x in types if x.slug ==           "refnorm"]), 1)
        self.assertEqual(len([x for x in types if x.slug ==               "obs"]), 1)
        self.assertEqual(len([x for x in types if x.slug == "possibly-replaces"]), 1)
        self.assertEqual(len([x for x in types if x.slug ==            "refold"]), 1)
        self.assertEqual(len([x for x in types if x.slug ==          "replaces"]), 1)
        self.assertEqual(len([x for x in types if x.slug ==           "updates"]), 1)
        self.assertEqual(len([x for x in types if x.slug ==            "refunk"]), 1)


    def test_mailing_list(self) -> None:
        ml = self.dt.mailing_list(MailingListURI("/api/v1/mailinglists/list/461/"))
        if ml is not None:
            self.assertEqual(ml.id,           461)
            self.assertEqual(ml.resource_uri, MailingListURI("/api/v1/mailinglists/list/461/"))
            self.assertEqual(ml.name,         "hackathon")
            self.assertEqual(ml.description,  "Discussion regarding past, present, and future IETF hackathons.")
            self.assertEqual(ml.advertised,   True)
        else:
            self.fail("Cannot find mailing list")


    def test_mailing_lists(self) -> None:
        ml = list(self.dt.mailing_lists())
        if ml is not None:
            self.assertNotEqual(len(ml), 0)
        else:
            self.fail("Cannot find mailing lists")


    def test_mailing_list_subscriptions(self) -> None:
        subs = list(self.dt.mailing_list_subscriptions("colin.perkins@glasgow.ac.uk"))
        self.assertEqual(len(subs), 1)
        self.assertEqual(subs[0].id,           66700)
        self.assertEqual(subs[0].resource_uri, MailingListSubscriptionsURI(uri="/api/v1/mailinglists/subscribed/66700/"))
        self.assertEqual(subs[0].email,        "colin.perkins@glasgow.ac.uk")
        self.assertEqual(subs[0].lists[0],     MailingListURI("/api/v1/mailinglists/list/461/"))


if __name__ == '__main__':
    unittest.main()

# =================================================================================================================================
# vim: set tw=0 ai:
