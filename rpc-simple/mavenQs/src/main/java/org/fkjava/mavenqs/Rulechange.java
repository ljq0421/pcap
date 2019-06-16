package org.fkjava.mavenqs;
import org.springframework.stereotype.Component;
import org.springframework.stereotype.Service;
import javax.websocket.OnClose;
import javax.websocket.OnMessage;
import javax.websocket.OnOpen;
import javax.websocket.Session;
import javax.websocket.server.ServerEndpoint;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.concurrent.CopyOnWriteArraySet;

@Service
@ServerEndpoint(value = "/change")
@Component

public class Rulechange {
    public static final int SUCCESS = 0;            // 表示程序执行成功

    public static final String SUCCESS_MESSAGE = "程序执行成功！";
    public static final String ERROR_MESSAGE = "程序执行出错：";
    //静态变量，用来记录当前在线连接数。应该把它设计成线程安全的。
    private static int onlineCount = 0;
    private static int messageCount=0;
    private static String[][] require=new String[20][20];
    //concurrent包的线程安全Set，用来存放每个客户端对应的MyWebSocket对象。
    private static CopyOnWriteArraySet<Rulechange> webSocketSet = new CopyOnWriteArraySet<Rulechange>();

    //与某个客户端的连接会话，需要通过它来给客户端发送数据
    private Session session;
    private static int messagenum=0;

    /**
     * 连接建立成功调用的方法*/
    @OnOpen
    public void onOpen(Session session) {
        this.session = session;
        webSocketSet.add(this);     //加入set中
        addOnlineCount();           //在线数加1
        resetMessageCount();
        System.out.println("rulechange 有新连接加入！当前在线人数为" + getOnlineCount());
        try {
            sendMessage("rulechange Hello,you are NO."+getOnlineCount());
        } catch (IOException e) {
            System.out.println("IO异常");
        }
    }

    /**
     * 连接关闭调用的方法
     */
    @OnClose
    public void onClose() {
        webSocketSet.remove(this);  //从set中删除
        subOnlineCount();           //在线数减1
        System.out.println("rulechange 有一连接关闭！当前在线人数为" + getOnlineCount());
    }

    /**
     * 收到客户端消息后调用的方法
     *
     * @param message 客户端发送过来的消息*/
    @OnMessage
    public void onMessage(String message, Session session) throws Exception {
        System.out.println("来自客户端的消息:" + message);
        require[onlineCount][messageCount] = message;
        addMessageCount();
        if (messageCount == 1 ) {//name,object,info
            String[] args1=new String[]{"python","/root/pcap/changerule.py",require[onlineCount][0]};
            //String COMMAND = "python /root/pcap/changerule.py ";    // 要执行的语句
            try {
                try {
                    //Process process = Runtime.getRuntime().exec(COMMAND + require[onlineCount][0]+" " + require[onlineCount][1]+" "+ require[onlineCount][2]);
                    //System.out.println(COMMAND + require[onlineCount][0]+" " + require[onlineCount][1]+" "+ require[onlineCount][2]);
                    Process process=Runtime.getRuntime().exec(args1);
                    System.out.println(args1[1]);
                    new Thread(new Runnable() {
                        @Override
                        public void run() {
                            BufferedReader br = new BufferedReader(
                                    new InputStreamReader(process.getInputStream()));
                            try {
                                while (br.readLine() != null)
                                    ;
                                br.close();
                            } catch (IOException e) {
                                e.printStackTrace();
                            }
                        }
                    }).start();
                    BufferedReader br = null;
                    br = new BufferedReader(new InputStreamReader(process.getErrorStream()));
                    String line = null;
                    while ((line = br.readLine()) != null) {
                        System.out.println(line);
                    }
                    process.waitFor();
                    br.close();
                    process.destroy();

            } catch (Exception e) {
                    e.printStackTrace();
                }
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
        else{
            sendMessage("hello");
        }
    }
    public void sendMessage(String message) throws IOException {
        this.session.getBasicRemote().sendText(message);
    }

    public static synchronized int getOnlineCount() {
        return onlineCount;
    }

    public static synchronized void addOnlineCount() {
        Rulechange.onlineCount++;
    }

    public static synchronized void subOnlineCount() {
        Rulechange.onlineCount--;
    }

    public static synchronized void resetMessageCount() {
        messageCount=0;
    }

    public static synchronized void addMessageCount() {
        Rulechange.messageCount++;
    }

}

