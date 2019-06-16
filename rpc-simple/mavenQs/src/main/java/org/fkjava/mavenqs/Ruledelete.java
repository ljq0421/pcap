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
@ServerEndpoint(value = "/ruledelete")
@Component
public class Ruledelete {// implements HelloService {

    //静态变量，用来记录当前在线连接数。应该把它设计成线程安全的。
    private static int onlineCount = 0;
    private static int messageCount=0;
    private static String[][] require=new String[20][255];
    //concurrent包的线程安全Set，用来存放每个客户端对应的MyWebSocket对象。
    private static CopyOnWriteArraySet<Ruledelete> webSocketSet = new CopyOnWriteArraySet<Ruledelete>();

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
        //System.out.println(messageCount);
        String COMMAND = "python /root/pcap/ruledelete.py ";
        if(messageCount==1){
            //0: "rule1 demo1-4,demo1-5 SSH告警:源ip:10.10.87.22;目的ip:10.10.87.21;端口号:22;方向:出;生效时间:0:00-1:00 open close"
            try{
                //System.out.println(messageCount);
                //if(messageCount==2){
                //Runtime.getRuntime().exec("python /root/pcap/truncatedb.py");
                //System.out.println("python /root/pcap/truncatedb.py");
                //}
                Process process = Runtime.getRuntime().exec(COMMAND+require[onlineCount][messageCount-1]);
                System.out.println(COMMAND+require[onlineCount][messageCount-1]);
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

    /**
     * 群发自定义消息
     * */
    public static void sendInfo(String message) throws IOException {
        for (Ruledelete item : webSocketSet) {
            try {
                item.sendMessage(message);
            } catch (IOException e) {
                continue;
            }
        }
    }


    public static synchronized int getOnlineCount() {
        return onlineCount;
    }

    public static synchronized void addOnlineCount() {
        Ruledelete.onlineCount++;
    }

    public static synchronized void subOnlineCount() {
        Ruledelete.onlineCount--;
    }

    public static synchronized void resetMessageCount() {
        messageCount=0;
    }

    public static synchronized void addMessageCount() {
        Ruledelete.messageCount++;
    }

}

