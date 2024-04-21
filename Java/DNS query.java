
import java.net.InetAddress;
import java.net.UnknownHostException;

public static void main(String[] args) throws UnknownHostException {
    /* 'getAllByName' will use the system configured 'resolver' */
    for (InetAddress ip : InetAddress.getAllByName("www.kame.net"))
        System.out.println(ip.getHostAddress());
}
