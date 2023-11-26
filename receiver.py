from colorama import init, Fore


class ReceiverProcess:
    """ Represent the receiver process in the application layer  """
    __buffer = list()

    @staticmethod
    def deliver_data(data):
        """ deliver data from the transport layer RDT receiver to the application layer
        :param data: a character received by the RDT RDT receiver
        :return: no return value
        """
        ReceiverProcess.__buffer.append(data)
        return

    @staticmethod
    def get_buffer():
        """ To get the message the process received over the network
        :return:  a python list of characters represent the incoming message
        """
        return ReceiverProcess.__buffer


class RDTReceiver:
    """" Implement the Reliable Data Transfer Protocol V2.2 Receiver Side """

    def __init__(self):
        self.sequence = '0'

    def get_sequence(self):
        return self.sequence

    @staticmethod
    def is_corrupted(packet):
        """ Check if the received packet from sender is corrupted or not
            :param packet: a python dictionary represent a packet received from the sender
            :return: True -> if the reply is corrupted | False ->  if the reply is NOT corrupted
        """
        # TODO provide your own implementation
        # print(packet['checksum'], "checksum11")
        # print(ord(packet['data']), "ascii ack11")
        return not packet['checksum'] == ord(packet['data'])
        pass

    @staticmethod
    def is_expected_seq(rcv_pkt, exp_seq):
        """ Check if the received reply from receiver has the expected sequence number
         :param rcv_pkt: a python dictionary represent a packet received by the receiver
         :param exp_seq: the receiver expected sequence number '0' or '1' represented as a character
         :return: True -> if ack in the reply match the   expected sequence number otherwise False
        """
        # TODO provide your own implementation
        # print(rcv_pkt['sequence_number'] ,"ack reply11")
        # print(exp_seq , "expected seq11")
        return rcv_pkt['sequence_number'] == exp_seq
        pass

    @staticmethod
    def make_reply_pkt(seq, checksum):
        """ Create a reply (feedback) packet with to acknowledge the received packet
        :param seq: the sequence number '0' or '1' to be acknowledged
        :param checksum: the checksum of the ack the receiver will send to the sender
        :return:  a python dictionary represent a reply (acknowledgement)  packet
        """
        reply_pck = {
            'ack': seq,
            'checksum': checksum
        }
        return reply_pck

    def rdt_rcv(self, rcv_pkt):
        """  Implement the RDT v2.2 for the receiver
        :param rcv_pkt: a packet delivered by the network layer 'udt_send()' to the receiver
        :return: the reply packet
        """
        # TODO provide your own implementation
        reply_pkt = {}
        rec_seq_num = ''
        # if self.is_corrupted(rcv_pkt, self):
        if self.is_corrupted(rcv_pkt) or not self.is_expected_seq(rcv_pkt, self):
            print(f"{Fore.RED}network_layer: corruption occurred {rcv_pkt} {Fore.RESET} ")
            corr_ack_seq_detector = '0' if self.sequence == '1' else '1'
            rec_seq_num = self.sequence
            reply_pkt = self.make_reply_pkt(corr_ack_seq_detector,
                                            ord(corr_ack_seq_detector))
        else:
            rec_seq_num = rcv_pkt['sequence_number']
            reply_pkt = self.make_reply_pkt(rec_seq_num,
                                            ord(rec_seq_num))
            self.sequence = '0' if rec_seq_num == '1' else '1'
        expecting_seq = rec_seq_num
        print(f"{Fore.GREEN}Receiver: Expected sequence number:{Fore.RESET} {expecting_seq}")
        print(f"{Fore.GREEN}Receiver: reply with{Fore.RESET}: {reply_pkt}")

        # deliver the data to the process in the application layer
        ReceiverProcess.deliver_data(rcv_pkt['data'])
        return reply_pkt
