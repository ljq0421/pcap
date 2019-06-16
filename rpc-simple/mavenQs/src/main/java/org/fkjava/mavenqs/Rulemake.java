package org.fkjava.mavenqs;

import org.springframework.stereotype.Component;
import org.springframework.stereotype.Service;

import javax.websocket.*;
import javax.websocket.server.ServerEndpoint;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.concurrent.CopyOnWriteArraySet;

@Service
@ServerEndpoint(value = "/rule_make")
@Component
public class Rulemake {// implements HelloService {

    //静态变量，用来记录当前在线连接数。应该把它设计成线程安全的。
    private static int onlineCount = 0;
    private static int messageCount=0;
    private static String[][] require=new String[20][255];
    //concurrent包的线程安全Set，用来存放每个客户端对应的MyWebSocket对象。
    private static CopyOnWriteArraySet<Rulemake> webSocketSet = new CopyOnWriteArraySet<Rulemake>();

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
        System.out.println("有新连接加入！当前在线人数为" + getOnlineCount());
        try {
            sendMessage("Hello,you are NO."+getOnlineCount());
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
        System.out.println("有一连接关闭！当前在线人数为" + getOnlineCount());
    }

    /**
     * 收到客户端消息后调用的方法
     *
     * @param message 客户端发送过来的消息*/
    @OnMessage
    public void onMessage(String message, Session session) throws Exception {
        System.out.println("来自客户端的消息:" + message);
        require[onlineCount][messageCount]=message;
        addMessageCount();
        String COMMAND1 = "python /root/pcap/makerule.py ";
        String COMMAND2 = "python /root/pcap/define.py ";
        if(message.equals("open") || message.equals("close")){//ruleid、规则名、对象、info、状态
            try{
                Process process1 = Runtime.getRuntime().exec(COMMAND1+require[onlineCount][0] + " "+require[onlineCount][1]+ " "+require[onlineCount][2] + " " +require[onlineCount][3]+ " " +require[onlineCount][4]);
                System.out.println(COMMAND1+require[onlineCount][0] + " "+require[onlineCount][1]+ " "+require[onlineCount][2] + " " +require[onlineCount][3]+ " " +require[onlineCount][4]);
                Process process2 = Runtime.getRuntime().exec(COMMAND2+require[onlineCount][0] + " "+require[onlineCount][1]+ " "+require[onlineCount][2] + " " +require[onlineCount][3]+ " " +require[onlineCount][4]);
                System.out.println(COMMAND2+require[onlineCount][0] + " "+require[onlineCount][1]+ " "+require[onlineCount][2] + " " +require[onlineCount][3]+ " " +require[onlineCount][4]);
                new Thread(new Runnable() {
                    @Override
                    public void run() {
                        BufferedReader br1 = new BufferedReader(new InputStreamReader(process1.getInputStream()));
                        BufferedReader br2 = new BufferedReader(new InputStreamReader(process2.getInputStream()));
                        try {
                            while (br1.readLine() != null);
                            br1.close();
                            while (br2.readLine() != null);
                            br2.close();
                        } catch (IOException e) {
                            e.printStackTrace();
                        }
                    }
                }).start();
                BufferedReader br1 = null;
                br1 = new BufferedReader(new InputStreamReader(process1.getErrorStream()));
                String line1 = null;
                while ((line1 = br1.readLine()) != null) {
                    System.out.println(line1);
                }
                process1.waitFor();
                br1.close();
                process1.destroy();
                BufferedReader br2 = null;
                br2 = new BufferedReader(new InputStreamReader(process2.getErrorStream()));
                String line2 = null;
                while ((line2 = br2.readLine()) != null) {
                    System.out.println(line2);
                }
                process2.waitFor();
                br2.close();
                process2.destroy();
            }catch (Exception e) {
                e.printStackTrace();
            }
        }
    }
    /**
     * 发生错误时调用*/
    @OnError
    public void onError(Session session, Throwable error) {
        System.out.println("发生错误");
        error.printStackTrace();
    }

    public void sendMessage(String message) throws IOException {
        this.session.getBasicRemote().sendText(message);
    }

    public static synchronized int getOnlineCount() {
        return onlineCount;
    }

    public static synchronized void addOnlineCount() {
        Rulemake.onlineCount++;
    }

    public static synchronized void subOnlineCount() {
        Rulemake.onlineCount--;
    }

    public static synchronized void resetMessageCount() {
        messageCount=0;
    }

    public static synchronized void addMessageCount() {
        Rulemake.messageCount++;
    }

}

