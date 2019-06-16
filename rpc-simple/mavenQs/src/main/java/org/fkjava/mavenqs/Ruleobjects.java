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
import java.io.InputStream;
import java.io.InputStreamReader;
import java.util.concurrent.CopyOnWriteArraySet;

@Service
@ServerEndpoint(value = "/ruleobjects")
@Component

public class Ruleobjects {

    private static CopyOnWriteArraySet<Ruleobjects> webSocketSet = new CopyOnWriteArraySet<Ruleobjects>();
    //与某个客户端的连接会话，需要通过它来给客户端发送数据
    private Session session;
    /**
     * 连接建立成功调用的方法*/
    @OnOpen
    public void onOpen(Session session) {
        System.out.println("jiaru11");
	this.session = session;
        webSocketSet.add(this);     //加入set中
    }

    /**
     * 连接关闭调用的方法
     */
    @OnClose
    public void onClose() {
        webSocketSet.remove(this);  //从set中删除
    }

    /**
     * 收到客户端消息后调用的方法
     *
     * @param message 客户端发送过来的消息*/
    @OnMessage
    public void onMessage(String message, Session session) throws Exception {
        System.out.println("来自客户端的消息:" + message);
        String COMMAND = "python /root/pcap/ruleobject.py "+message;    // 要执行的语句
        try {
            try {
                Process process = Runtime.getRuntime().exec(COMMAND);
                System.out.println(COMMAND);
                String line=null;
                InputStream is = process.getInputStream();
                InputStreamReader isr = new InputStreamReader(is);
                BufferedReader br = new BufferedReader(isr);
                while ((line = br.readLine()) != null) {
                    System.out.println(line);
                    System.out.flush();
                    sendMessage(line);
                }
                isr.close();
                br.close();
                is.close();
            } catch (Exception e) {
                e.printStackTrace();
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public void sendMessage(String message) throws IOException {
        this.session.getBasicRemote().sendText(message);
    }

}

