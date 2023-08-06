// SPDX-FileCopyrightText: 2021 Carl Schwan <carlschwan@kde.org>
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick 2.7
import org.kde.kirigami 2.5 as Kirigami
import QtQuick.Controls 2.5
import QtQuick.Layouts 1.3
import Glucose 0.1

Kirigami.Page {
    id: glucosePage
    title: qsTr("Blood Glucose Level")

    Glucose { // Glucose object registered at main.py
        id: blood_glucose
        onSetOK: {
            /* We pop the current page from the stack and immediately
            /  replace the Biopage to refresh its contents
            */
            pageStack.pop()
            pageStack.replace(Qt.resolvedUrl("PageBio.qml"))
        }
    }

    Rectangle {
        anchors.top: parent.top
        anchors.horizontalCenter: parent.horizontalCenter
        color: "#136f84"
        height: 80
        width: parent.width
        radius: 10
        Image {
            id: glucoseIcon
            height: parent.height
            anchors.centerIn: parent
            source: "../images/glucose-icon.svg"
            fillMode: Image.PreserveAspectFit
        }
    }

    ColumnLayout {
        id: content
        anchors.centerIn: parent
        Label {
            Layout.alignment: Qt.AlignHCenter
            text: qsTr("Blood glucose level")
            font.bold: true
        }

        SpinBox {
            id: txtGlucose
            Layout.alignment: Qt.AlignHCenter
            Layout.preferredHeight: 100
            Layout.preferredWidth: 150
            font.pixelSize:30
            from: 10
            to: 800
            value:90
            editable: true
            inputMethodHints: Qt.ImhDigitsOnly
            wheelEnabled: true
        }

        Button {
            id: buttonSetGlucose
            Layout.alignment: Qt.AlignHCenter
            text: qsTr("Set")
            icon.name: "list-add"
            onClicked: blood_glucose.getvals(txtGlucose.value);
        }
    }
   footer: Rectangle{
            id: rectfooter
            width: parent.width
            height: 40
            Image {
                id: myghIcon
                anchors.centerIn: rectfooter
                source: "../images/myGH-horizontal-icon.svg"
                width: 160
                fillMode: Image.PreserveAspectFit
            }
        }


}
