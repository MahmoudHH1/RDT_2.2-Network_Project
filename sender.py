from colorama import init, Fore


class SenderProcess:
    """ Represent the sender process in the application layer  """

    __buffer = list()

    @staticmethod
    def set_outgoing_data(buffer):
        """ To set the message the process would send out over the network
        :param buffer:  a python list of characters represent the outgoing message
        :return: no return value
        """
        SenderProcess.__buffer = buffer
        return

    @staticmethod
    def get_outgoing_data():
        """ To get the message the process would send out over the network
        :return:  a python list of characters represent the outgoing message
        """
        return SenderProcess.__buffer


class RDTSender:
    """ Implement the Reliable Data Transfer Protocol V2.2 Sender Side """

    def __init__(self, net_srv):
        """ This is a class constructor
            It initializes the RDT sender sequence number  to '0' and the network layer services
            The network layer service provide the method udt_send(send_pkt)
        """
        self.sequence = '0'
        self.net_srv = net_srv

    @staticmethod
    def get_checksum(data):
        """ Calculate the checksum for outgoing data
        :param data: one and only one character, for example data = 'A'
        :return: the ASCII code of the character, for example ASCII('A') = 65
        """
        checksum = ord(data)
        return checksum

    @staticmethod
    def clone_packet(packet):
        """ Make a copy of the outgoing packet
        :param packet: a python dictionary represent a packet
        :return: return a packet as python dictionary
        """
        pkt_clone = {
            'sequence_number': packet['sequence_number'],
            'data': packet['data'],
            'checksum': packet['checksum']
        }
        return pkt_clone

    def get_sequence(self):
        return self.sequence

    @staticmethod
    def is_corrupted(reply):
        """ Check if the received reply from receiver is corrupted or not
        :param reply: a python dictionary represent a reply sent by the receiver
        :return: True -> if the reply is corrupted | False ->  if the reply is NOT corrupted
        """
        # print(reply['checksum'] , "checksum1")
        # print(ord(reply['ack'] ), "ascii ack1" )
        return reply['checksum'] != ord(reply['ack'])
        pass

    @staticmethod
    def is_expected_seq(reply, exp_seq):
        """ Check if the received reply from receiver has the expected sequence number
        :param reply: a python dictionary represent a reply sent by the receiver
        :param exp_seq: the sender expected sequence number '0' or '1' represented as a character
        :return: True -> if ack in the reply match the   expected sequence number otherwise False
        """
        # print(reply['ack'] , "ack reply1")
        # print(exp_seq , "expected seq1")
        return reply['ack'] == exp_seq
        pass

    @staticmethod
    def make_pkt(seq, data, checksum):
        """ Create an outgoing packet as a python dictionary
        :param seq: a character represent the sequence number of the packet, the one expected by the receiver '0' or '1'
        :param data: a single character the sender want to send to the receiver
        :param checksum: the checksum of the data the sender will send to the receiver
        :return: a python dictionary represent the packet to be sent
        """
        packet = {
            'sequence_number': seq,
            'data': data,
            'checksum': checksum
        }
        return packet

    def rdt_send(self, process_buffer):
        """ Implement the RDT v2.2 for the sender
        :param process_buffer:  a list storing the message the sender process wish to send to the receiver process
        :return: terminate without returning any value
        """
        # for every character in the buffer
        for data in process_buffer:
            checksum = RDTSender.get_checksum(data)
            pkt = RDTSender.make_pkt(self.sequence, data, checksum)
            clonedPacket = self.clone_packet(pkt)
            print(f"{Fore.BLUE}Sender: expected sequence number:{Fore.RESET} {self.sequence}")
            print(f"{Fore.BLUE}Sender: sending:{Fore.RESET} {pkt}")
            reply = self.net_srv.udt_send(pkt)
            # print(reply['checksum'], "checksum3")
            # print(ord(reply['ack']), "ascii ack3")
            seqNumBeforeCorruption = self.sequence
            # if not ord(reply['ack']) == reply['checksum']:  # reply corrupted
            #    print(f"{Fore.RED}network_layer: corruption occurred {reply} {Fore.RESET} ")
            print(f"{Fore.BLUE}Sender: received :{Fore.RESET} {reply} ")
            while ((not self.is_expected_seq(reply, self.sequence)) or
                   self.is_corrupted(reply)):
                print(f"{Fore.BLUE}Sender: expected sequence number:{Fore.RESET} {clonedPacket['sequence_number']}")
                print(f"{Fore.BLUE}Sender: sending:{Fore.RESET} {clonedPacket}")
                pkt = self.clone_packet(clonedPacket)
                reply = self.net_srv.udt_send(pkt)
                #    if self.is_corrupted(reply, self):
                #        print(f"{Fore.RED}network_layer: corruption occurred {reply} {Fore.RESET} ")
                print(f"{Fore.BLUE}Sender: received :{Fore.RESET} {reply} ")
            self.sequence = '0' if seqNumBeforeCorruption == '1' else '1'
        print(f'Sender Done!')
        return
