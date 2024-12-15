📦 Reliable Data Transfer Protocol v2.2

🎯 Project Overview

This repository contains the implementation of the Reliable Data Transfer Protocol (RDT) v2.2. The protocol was designed to enhance understanding of reliable data transfer mechanisms and was implemented as part of the CSEN503 coursework.

✨ Key Characteristics of RDTv2.2:

🚦 Stop-and-wait protocol.

✅ Positive acknowledgment with retransmission.

🔄 Alternating bit protocol (1-bit sequence numbers).

📦 Handles packet corruption.

🚫 Does not handle packet loss or out-of-order delivery.

📂 Repository Structure

main.py - The main script to start and test the RDTv2.2 protocol.

sender.py - Implements the sender side of the RDTv2.2 protocol.

receiver.py - Implements the receiver side of the RDTv2.2 protocol.

network.py - Simulates the network layer for delivering packets and acknowledgments.

📜 Protocol Details

Finite State Machine (FSM) Diagrams

Sender Side:


Receiver Side:


Pseudo-code

Receiver Side

Check if the received packet is corrupted or has an unexpected sequence number.

If true:

Display the corrupted packet.

Update the sequence number.

Create and return a corrupted packet.

Else:

Add the data to the buffer.

Create and return a new acknowledgment packet.

Sender Side

Loop through each character in the buffer:

Create and send packets with the appropriate sequence number.

Retransmit packets if corruption or mismatched sequence numbers are detected.

Complete transmission and print Sender Done.

🛠 Additions to network.py

Printed corruption details for packets or replies if corruption occurred in the udt_send method.

Added a method to adjust delays while sending messages: __corrupt_delay.

Implemented timeout handling (2 seconds) as part of a bonus feature.

✅ Test Cases

Sending "HE" with reliability = 1.

Sending "HE" with reliability = 0.7.

Sending "TEST" with reliability = 0.5.

Sending "TEST" with reliability = 0.2.

🏁 Conclusion

The implementation of RDTv2.2 successfully transmits messages to the intended receiver under various reliability conditions, meeting the protocol's objectives.

📬 Submission Instructions

Ensure the following files are included:

main.py

sender.py

receiver.py

network.py

Project Report with:

FSM diagrams

Pseudo-code

Implementation details

Test case execution results

🛑 Note: Adhere to the academic integrity guidelines provided in the project description.

Enjoy exploring RDTv2.2! 🚀
